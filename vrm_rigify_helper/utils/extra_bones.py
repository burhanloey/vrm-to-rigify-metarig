import bpy

from ..checks import is_rigify_rig
from ..common import get_current_visible_layers, layer_params
from ..layers import HAIR_LAYER, CLOTH_LAYER, IK_LAYERS
    
    
def set_tail_follow(context, value, layer):
    rig = context.view_layer.objects.active
    
    initial_layers_visibility = get_current_visible_layers(context)
    
    bpy.ops.object.mode_set(mode='POSE')
    
    bpy.ops.pose.select_all(action='DESELECT')
    
    # Only make the selected layer visible
    rig.data.layers = layer_params([layer])
    
    bpy.ops.pose.select_all(action='SELECT')
    
    # Make any bone active so Rigify will show their properties in the panel
    if context.selected_pose_bones:
        rig.data.bones.active = context.selected_pose_bones[0].bone
    
    for bone in context.selected_pose_bones:
        if ('tail_follow' in bone):
            bone['tail_follow'] = value
            
    rig.data.layers = initial_layers_visibility
    
    
def set_all_ik_stretch(context, value):
    rig = context.view_layer.objects.active
    
    initial_layers_visibility = get_current_visible_layers(context)
    
    bpy.ops.object.mode_set(mode='POSE')
    
    bpy.ops.pose.select_all(action='DESELECT')
    
    # Only make IK layers visible
    rig.data.layers = layer_params(IK_LAYERS)
    
    bpy.ops.pose.select_all(action='SELECT')
    
    # Make any bone active so Rigify will show their properties in the panel
    if context.selected_pose_bones:
        rig.data.bones.active = context.selected_pose_bones[0].bone
        
    for bone in context.selected_pose_bones:
        if ('IK_Stretch' in bone):
            bone['IK_Stretch'] = value
            
    rig.data.layers = initial_layers_visibility


class BaseSetTailFollow(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}

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
        
        
class EnableAllIKStretch(BaseSetTailFollow):
    """Enable IK stretch on all IK controls"""
    bl_idname = "vrm_rigify_helper.enable_all_ik_stretch"
    bl_label = "Enable All IK Stretch"

    def execute(self, context):
        set_all_ik_stretch(context, 1.0)
        return {'FINISHED'}
        
        
class DisableAllIKStretch(BaseSetTailFollow):
    """Disable IK stretch on all IK controls"""
    bl_idname = "vrm_rigify_helper.disable_all_ik_stretch"
    bl_label = "Disable All IK Stretch"

    def execute(self, context):
        set_all_ik_stretch(context, 0.0)
        return {'FINISHED'}
