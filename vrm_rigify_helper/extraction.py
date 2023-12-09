import bpy

from .checks import is_vrm_rig
from .utils import select_all_root_bones


def extract_vrm_extra_bones(context, vroid_rig, pattern, bone_layer, name_suffix):
    vroid_rig.select_set(True)
    context.view_layer.objects.active = vroid_rig
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.duplicate()
    
    hair_rig = context.view_layer.objects.active
    
    # Delete other bones that are not selected by pattern
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.select_pattern(pattern=pattern, extend=False)
    bpy.ops.armature.select_all(action='INVERT')
    bpy.ops.armature.delete()
    bpy.ops.armature.select_all(action='SELECT')
    
    for bone in context.selected_editable_bones:
        bone['extracted_vrm_bone'] = name_suffix
    
    # Move bones to designated bone layer
    bone_layers_parameter = [False] * 32
    bone_layers_parameter[bone_layer] = True
    bpy.ops.armature.bone_layers(layers=bone_layers_parameter)
    hair_rig.data.layers = bone_layers_parameter  # make the layer visible
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    new_armature = context.view_layer.objects.active
    new_armature.name = vroid_rig.name + '.' + name_suffix
    
    return new_armature
    
    
def extract_vrm_hair(context, vroid_rig):
    return extract_vrm_extra_bones(context, vroid_rig, '*hair*', 19, 'hair')


def extract_vrm_skirt(context, vroid_rig):
    return extract_vrm_extra_bones(context, vroid_rig, '*skirt*', 21, 'skirt')
    
    
def setup_bones_as_rigify_tail(context, armature, tweak_layer):
    context.view_layer.objects.active = armature
    
    bpy.ops.object.mode_set(mode='POSE')
    
    select_all_root_bones(context)
    
    root_bones = context.selected_pose_bones
    
    bone_layers_parameter = [False] * 32
    bone_layers_parameter[tweak_layer] = True
    
    for root_bone in root_bones:
        root_bone.rigify_type = 'spines.basic_tail'
        
        # Automation axes, 0 = x-axis, 1 = y-axis, 2 = z-axis
        root_bone.rigify_parameters.copy_rotation_axes[0] = True
        root_bone.rigify_parameters.copy_rotation_axes[1] = True
        root_bone.rigify_parameters.copy_rotation_axes[2] = True
        
        # Assign tweak layers
        root_bone.rigify_parameters.tweak_layers_extra = True
        root_bone.rigify_parameters.tweak_layers = bone_layers_parameter
        
        
def setup_vrm_hair_bones_as_rigify_tail(context, hair_rig):
    setup_bones_as_rigify_tail(context, hair_rig, 20)
    
    
def setup_vrm_skirt_bones_as_rigify_tail(context, skirt_rig):
    setup_bones_as_rigify_tail(context, skirt_rig, 22)
    
    
def split_coat_bones_from_skirt_rig(context, skirt_rig):
    skirt_rig.select_set(True)
    context.view_layer.objects.active = skirt_rig
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.object.select_pattern(pattern='*coat*', extend=False)
    
    for bone in context.selected_editable_bones:
        bone['extracted_vrm_bone'] = 'coat_skirt'
    
    bpy.ops.armature.separate(confirm=False)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # After separated, the original armature (skirt rig) will be active, and
    # the new armature (coat skirt rig) will be selected but not active.
    # To access the coat skirt rig, I just deselect the active armature and
    # access the only selected armature from the list.
    
    context.view_layer.objects.active.select_set(False)
    
    coat_rig = context.view_layer.objects.selected[0]
    coat_rig.name = skirt_rig.name + '.coat'
    
    return coat_rig


def extract_vrm_extra_bones_as_rigify(context):
    vroid_rig = context.view_layer.objects.active
    
    hair_rig = extract_vrm_hair(context, vroid_rig)
    setup_vrm_hair_bones_as_rigify_tail(context, hair_rig)
    hair_rig.data['extracted_vrm_rig'] = 'hair'
    
    skirt_rig = extract_vrm_skirt(context, vroid_rig)
    setup_vrm_skirt_bones_as_rigify_tail(context, skirt_rig)
    skirt_rig.data['extracted_vrm_rig'] = 'skirt'
    
    coat_rig = split_coat_bones_from_skirt_rig(context, skirt_rig)
    coat_rig.data['extracted_vrm_rig'] = 'coat_skirt'
    
    bpy.ops.object.select_all(action='DESELECT')
    
    hair_rig.select_set(True)
    skirt_rig.select_set(True)
    coat_rig.select_set(True)
    
    context.view_layer.objects.active = hair_rig
    
    
class ExtractVRMExtraBonesAsRigify(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "vrm_rigify_helper.extract_vrm_extra_bones_as_rigify"
    bl_label = "Extract VRM Extra Bones as Rigify"

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_vrm_rig(obj)

    def execute(self, context):
        extract_vrm_extra_bones_as_rigify(context)
        return {'FINISHED'}