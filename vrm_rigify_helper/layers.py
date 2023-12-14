import bpy

from .checks import is_metarig


HAIR_LAYER = 19
HAIR_TWEAK_LAYER = 20
CLOTH_LAYER = 21
CLOTH_TWEAK_LAYER = 22

HAIR_UI_ROW = 13
HAIR_TWEAK_UI_ROW = 14
CLOTH_UI_ROW = 13
CLOTH_TWEAK_UI_ROW = 14

# Group 5 = FK, Group 4 = Tweak
HAIR_GROUP = 5
HAIR_TWEAK_GROUP = 4
CLOTH_GROUP = 5
CLOTH_TWEAK_GROUP = 4

HAIR_UI_TEXT = 'Hair'
HAIR_TWEAK_UI_TEXT = 'Hair (Tweak)'
CLOTH_UI_TEXT = 'Cloth'
CLOTH_TWEAK_UI_TEXT = 'Cloth (Tweak)'


def update_metarig_bone_layers(context):
    metarig = context.view_layer.objects.active

    # Hair
    metarig.data.layers[HAIR_LAYER] = True  # make visible
    
    hair_layer = metarig.data.rigify_layers[HAIR_LAYER]
    hair_layer.name = HAIR_UI_TEXT
    hair_layer.row = HAIR_UI_ROW
    hair_layer.group = HAIR_GROUP
    
    # Hair (Tweak)
    hair_tweak_layer = metarig.data.rigify_layers[HAIR_TWEAK_LAYER]
    hair_tweak_layer.name = HAIR_TWEAK_UI_TEXT
    hair_tweak_layer.row = HAIR_TWEAK_UI_ROW
    hair_tweak_layer.group = HAIR_TWEAK_GROUP
    
    # Cloth
    metarig.data.layers[CLOTH_LAYER] = True  # make visible
    
    cloth_layer = metarig.data.rigify_layers[CLOTH_LAYER]
    cloth_layer.name = CLOTH_UI_TEXT
    cloth_layer.row = CLOTH_UI_ROW
    cloth_layer.group = CLOTH_GROUP
    
    # Cloth (Tweak)
    cloth_tweak_layer = metarig.data.rigify_layers[CLOTH_TWEAK_LAYER]
    cloth_tweak_layer.name = CLOTH_TWEAK_UI_TEXT
    cloth_tweak_layer.row = CLOTH_TWEAK_UI_ROW
    cloth_tweak_layer.group = CLOTH_TWEAK_GROUP


class UpdateMetarigBoneLayers(bpy.types.Operator):
    """Hair and its tweak at layer 19 and 20. Cloth and its tweak at layer 21 and 22"""
    bl_idname = "vrm_rigify_helper.update_metarig_bone_layers"
    bl_label = "Update Metarig Bone Layers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        update_metarig_bone_layers(context)
        return {'FINISHED'}
