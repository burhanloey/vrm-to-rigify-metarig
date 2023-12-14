import bpy

from .checks import is_rigify_rig
from .common import get_current_visible_layers, layer_params, bone_select_set


UNUSED_DEFORM_BONES = [
    'ear',
    'teeth',
    'nose',
    'lid',
    'tongue',
    'jaw_master',
    'chin',
    'jaw',
    'lip',
    'brow',
    'cheek',
    'forehead',
    'temple'
]

DEFORM_LAYER = 29
FACE_BONE_LAYERS = [0, 1, 2]


def select_facial_bone_layers(context):
    rig = context.view_layer.objects.active
    rig.data.layers = layer_params(FACE_BONE_LAYERS)
        
        
def select_deform_bone_layer(context):
    rig = context.view_layer.objects.active
    rig.data.layers = layer_params([DEFORM_LAYER])


def delete_unused_control_bones(context):
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Delete all other than eye bones
    bpy.ops.object.select_pattern(pattern='*eye*', extend=False)
    bpy.ops.armature.select_all(action='INVERT')
    bpy.ops.armature.delete(confirm=False)
    
    
def hide_eye_master_control_bone(context):
    bpy.ops.object.mode_set(mode='POSE')
    
    bpy.ops.object.select_pattern(pattern='*master*', extend=False)
    bpy.ops.pose.hide(unselected=False)
    
    
def delete_unused_deform_bones(context):
    rig = context.view_layer.objects.active
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='SELECT')
    
    bones = context.selected_editable_bones
    
    # Deselect bone not in unused bone list (Select bone in unused list)
    for bone in bones:
        part_name = bone.name.replace('DEF-', '').split('.')[0]
        
        if part_name not in UNUSED_DEFORM_BONES:
            bone_select_set(bone, False)
            
    bpy.ops.armature.delete(confirm=False)


def remove_unused_bones(context):
    rig = context.view_layer.objects.active
    
    initial_mode = rig.mode
    initial_visible_layers = get_current_visible_layers(context)
    
    # Facial control cleanup
    select_facial_bone_layers(context)
    delete_unused_control_bones(context)
    hide_eye_master_control_bone(context)
    
    # Unused facial deform bones cleanup
    select_deform_bone_layer(context)
    delete_unused_deform_bones(context)
    
    # Reset bone layers selection
    rig.data.layers = initial_visible_layers
    
    bpy.ops.object.mode_set(mode=initial_mode)


class RemoveUnusedBones(bpy.types.Operator):
    """Remove mostly the facial bones since facial expressions are done with shape keys"""
    bl_idname = "vrm_rigify_helper.remove_unused_bones"
    bl_label = "Remove Unused Bones"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_rigify_rig(obj)

    def execute(self, context):
        remove_unused_bones(context)
        return {'FINISHED'}
