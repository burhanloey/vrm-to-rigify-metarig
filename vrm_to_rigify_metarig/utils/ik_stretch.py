import bpy

from ..checks import is_rigify_rig
from ..common import get_current_visible_layers, layer_params
from ..layers import IK_LAYERS
    
    
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
        

class BaseIKStretchOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_rigify_rig(obj)


class EnableAllIKStretch(BaseIKStretchOperator):
    """Enable IK stretch on all IK controls"""
    bl_idname = "vrm_to_rigify_metarig.enable_all_ik_stretch"
    bl_label = "Enable All IK Stretch"

    def execute(self, context):
        set_all_ik_stretch(context, 1.0)
        return {'FINISHED'}
        
        
class DisableAllIKStretch(BaseIKStretchOperator):
    """Disable IK stretch on all IK controls"""
    bl_idname = "vrm_to_rigify_metarig.disable_all_ik_stretch"
    bl_label = "Disable All IK Stretch"

    def execute(self, context):
        set_all_ik_stretch(context, 0.0)
        return {'FINISHED'}
