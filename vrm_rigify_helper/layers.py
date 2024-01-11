import bpy

from .checks import is_metarig, is_rigify_rig
from .common import layer_params, BLENDER_LAYER_COUNT


FACE_LAYER = 0
TORSO_LAYER = 3
FINGERS_LAYER = 5

ARM_L_IK_LAYER = 7
ARM_L_FK_LAYER = 8
ARM_R_IK_LAYER = 10
ARM_R_FK_LAYER = 11

LEG_L_IK_LAYER = 13
LEG_R_IK_LAYER = 16

ROOT_LAYER = 28

DEFAULT_VISIBLE_LAYERS = [
    FACE_LAYER,
    TORSO_LAYER,
    FINGERS_LAYER,
    ARM_L_IK_LAYER,
    ARM_L_FK_LAYER,
    ARM_R_IK_LAYER,
    ARM_R_FK_LAYER,
    LEG_L_IK_LAYER,
    LEG_R_IK_LAYER,
    ROOT_LAYER
]

IK_LAYERS = [
    ARM_L_IK_LAYER,
    ARM_R_IK_LAYER,
    LEG_L_IK_LAYER,
    LEG_R_IK_LAYER
]
        
        
class ShowDefaultVisibleLayers(bpy.types.Operator):
    """Show default visible layers"""
    bl_idname = "vrm_to_rigify_metarig.show_default_visible_layers"
    bl_label = "Show Default Visible Layers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_rigify_rig(obj)

    def execute(self, context):
        rig = context.view_layer.objects.active
        rig.data.layers = layer_params(DEFAULT_VISIBLE_LAYERS)
        return {'FINISHED'}
        
        
class ShowAllControlLayers(bpy.types.Operator):
    """Show default visible layers"""
    bl_idname = "vrm_to_rigify_metarig.show_all_control_layers"
    bl_label = "Show All Control Layers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_rigify_rig(obj)

    def execute(self, context):
        rig = context.view_layer.objects.active
        
        all_control_layers = [False] * BLENDER_LAYER_COUNT
        
        for i in range(23):
            all_control_layers[i] = True
        all_control_layers[ROOT_LAYER] = True
        
        rig.data.layers = all_control_layers
        return {'FINISHED'}
