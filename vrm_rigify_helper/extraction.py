import bpy

from .checks import is_vrm_rig
from .utils.selection import select_all_root_bones
from .common import layer_params


def extract_vrm_extra_bones(context, vroid_rig, pattern, bone_layer, name_suffix):
    vroid_rig.select_set(True)
    context.view_layer.objects.active = vroid_rig
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.duplicate()
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.select_pattern(pattern=pattern, extend=False)
    
    # Delete the duplicated armature if no bones found and return None
    if not context.selected_editable_bones:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.delete(use_global=True, confirm=False)
        return None
    
    # Delete other bones that are not selected by pattern
    bpy.ops.armature.select_all(action='INVERT')
    bpy.ops.armature.delete()
    bpy.ops.armature.select_all(action='SELECT')
    
    # Tag the bones in custom properties for later use
    for bone in context.selected_editable_bones:
        bone['extracted_vrm_bone'] = name_suffix
    
    # Move bones to designated bone layer
    bone_layer_params = layer_params([bone_layer])
    bpy.ops.armature.bone_layers(layers=bone_layer_params)
    
    extracted_armature = context.view_layer.objects.active
    extracted_armature.data.layers = bone_layer_params  # make the layer visible
    extracted_armature.name = vroid_rig.name + '.' + name_suffix
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return extracted_armature
    
    
def extract_vrm_hair(context, vroid_rig):
    return extract_vrm_extra_bones(context, vroid_rig, '*hair*', 19, 'hair')


def extract_vrm_skirt(context, vroid_rig):
    return extract_vrm_extra_bones(context, vroid_rig, '*skirt*', 21, 'skirt')
    
    
def setup_bones_as_rigify_tail(context, armature, tweak_layer):
    context.view_layer.objects.active = armature
    
    bpy.ops.object.mode_set(mode='POSE')
    
    select_all_root_bones(context)
    
    root_bones = context.selected_pose_bones
    
    for bone in root_bones:
        bone.rigify_type = 'spines.basic_tail'
        
        # Automation axes, 0 = x-axis, 1 = y-axis, 2 = z-axis
        bone.rigify_parameters.copy_rotation_axes[0] = True
        bone.rigify_parameters.copy_rotation_axes[1] = True
        bone.rigify_parameters.copy_rotation_axes[2] = True
        
        # Assign tweak layers
        bone.rigify_parameters.tweak_layers_extra = True
        bone.rigify_parameters.tweak_layers = layer_params([tweak_layer])
        
        
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
    
    selected_objects = context.view_layer.objects.selected
    
    if selected_objects:
        coat_rig = selected_objects[0]
        coat_rig.name = skirt_rig.name + '.coat'
        return coat_rig
    else:
        return None


def extract_vrm_extra_bones_as_rigify(context):
    vroid_rig = context.view_layer.objects.active
    extracted_rigs = []
    
    # Extract hair rig
    hair_rig = extract_vrm_hair(context, vroid_rig)
    if hair_rig:
        setup_vrm_hair_bones_as_rigify_tail(context, hair_rig)
        hair_rig.data['extracted_vrm_rig'] = 'hair'
        extracted_rigs.append(hair_rig)
    
    # Extract skirt rig
    skirt_rig = extract_vrm_skirt(context, vroid_rig)
    if skirt_rig:
        setup_vrm_skirt_bones_as_rigify_tail(context, skirt_rig)
        skirt_rig.data['extracted_vrm_rig'] = 'skirt'
        extracted_rigs.append(skirt_rig)
    
        # Extract coat skirt rig from skirt rig
        coat_rig = split_coat_bones_from_skirt_rig(context, skirt_rig)
        if coat_rig:
            coat_rig.data['extracted_vrm_rig'] = 'coat_skirt'
            extracted_rigs.append(coat_rig)
    
    bpy.ops.object.select_all(action='DESELECT')
    
    if extracted_rigs:
        for rig in extracted_rigs:
            rig.select_set(True)
        context.view_layer.objects.active = extracted_rigs[0]
    
    
class ExtractVRMExtraBonesAsRigify(bpy.types.Operator):
    """Extract hair, skirt and coat skirt into separate rigs"""
    bl_idname = "vrm_rigify_helper.extract_vrm_extra_bones_as_rigify"
    bl_label = "Extract VRM Extra Bones"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_vrm_rig(obj)

    def execute(self, context):
        extract_vrm_extra_bones_as_rigify(context)
        return {'FINISHED'}
