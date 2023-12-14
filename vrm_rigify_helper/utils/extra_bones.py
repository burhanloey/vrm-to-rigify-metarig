import bpy

from ..checks import is_rigify_rig
from ..common import get_current_visible_layers


HAIR_LAYER = 19
CLOTH_LAYER = 21
    
    
def set_tail_follow(context, value, layer):
    rig = context.view_layer.objects.active
    
    initial_layers_visibility = get_current_visible_layers(context)
    
    bpy.ops.object.mode_set(mode='POSE')
    
    bpy.ops.pose.select_all(action='DESELECT')
    
    visible_layer_parameters = [False] * 32
    visible_layer_parameters[layer] = True
    
    rig.data.layers = visible_layer_parameters
    
    bpy.ops.pose.select_all(action='SELECT')
    
    if context.selected_pose_bones:
        rig.data.bones.active = context.selected_pose_bones[0].bone
    
    for bone in context.selected_pose_bones:
        if ('tail_follow' in bone):
            bone['tail_follow'] = value
            
    rig.data.layers = initial_layers_visibility


class BaseSetTailFollow(bpy.types.Operator):
    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_rigify_rig(obj)


class EnableHairFollow(BaseSetTailFollow):
    """Make hair tail bones follow the parent bones"""
    bl_idname = "vrm_rigify_helper.enable_hair_follow"
    bl_label = "Enable Hair Follow"

    def execute(self, context):
        set_tail_follow(context, 1.0, HAIR_LAYER)
        return {'FINISHED'}
        
        
class DisableHairFollow(BaseSetTailFollow):
    """Make hair tail bones not follow the parent bones"""
    bl_idname = "vrm_rigify_helper.disable_hair_follow"
    bl_label = "Disable Hair Follow"

    def execute(self, context):
        set_tail_follow(context, 0.0, HAIR_LAYER)
        return {'FINISHED'}
        
        
class EnableClothFollow(BaseSetTailFollow):
    """Make cloth tail bones follow the parent bones"""
    bl_idname = "vrm_rigify_helper.enable_cloth_follow"
    bl_label = "Enable Cloth Follow"

    def execute(self, context):
        set_tail_follow(context, 1.0, CLOTH_LAYER)
        return {'FINISHED'}
        
        
class DisableClothFollow(BaseSetTailFollow):
    """Make cloth tail bones not follow the parent bones"""
    bl_idname = "vrm_rigify_helper.disable_cloth_follow"
    bl_label = "Disable Cloth Follow"

    def execute(self, context):
        set_tail_follow(context, 0.0, CLOTH_LAYER)
        return {'FINISHED'}
