bl_info = {
    "name": "VRM To Rigify Metarig",
    "author": "burhanloey",
    "description": "Generate Rigify armature and metarig from VRM model",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "3D Viewport > VRM To Rigify Metarig Panel",
    "doc_url": "https://github.com/burhanloey/vrm-to-rigify-metarig",
    "tracker_url": "https://github.com/burhanloey/vrm-to-rigify-metarig/issues",
    "category": "Rigging",
}

import bpy

from .layers import ShowDefaultVisibleLayers, ShowAllControlLayers
from .cleanup import RemoveUnusedBones
from .corrections.head import AlignHeadBone
from .corrections.hand import AlignHandBones
from .corrections.feet import AlignFeetBones
from .utils.ik_stretch import EnableAllIKStretch, DisableAllIKStretch
from .utils.eye_fix import FixEyeDirection, RecalibrateEyeDirection
from .utils.modifiers import HideToonShaderInViewport, ShowToonShaderInViewport
from .utils.look_at import LookAtObjectConstraint, ClearLookAtConstraint
from .metarig import GenerateMetarig
from .main import OneClickSetup, Regenerate

from .checks import is_metarig


class VRMToRigifyMetarigMainPanel(bpy.types.Panel):
    """Generate Rigify armature and metarig from VRM model"""
    bl_label = "VRM To Rigify Metarig"
    bl_idname = "VRM_TO_RIGIFY_METARIG_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRM To Rigify Metarig"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.scale_y = 2.0
        
        obj = context.view_layer.objects.active
        
        if is_metarig(obj) and obj.data.rigify_target_rig:
            row.operator("vrm_to_rigify_metarig.regenerate", icon="OUTLINER_OB_ARMATURE")
        else:
            row.operator("vrm_to_rigify_metarig.one_click_setup", icon="OUTLINER_OB_ARMATURE")


class VRMToRigifyMetarigOperatorsPanel(bpy.types.Panel):
    """"""
    bl_label = "Operators"
    bl_idname = "VRM_TO_RIGIFY_METARIG_PT_operators_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRM To Rigify Metarig"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("vrm_to_rigify_metarig.generate_metarig")
        
        col = layout.column(align=True)
        col.label(text="Bone alignment:")
        col.operator("vrm_to_rigify_metarig.align_head_bone", text="Head")
        col.operator("vrm_to_rigify_metarig.align_hand_bones", text="Hand")
        col.operator("vrm_to_rigify_metarig.align_feet_bones", text="Feet")
        
        row = layout.row()
        row.operator("vrm_to_rigify_metarig.remove_unused_bones")
        
        row = layout.row()
        row.operator("vrm_to_rigify_metarig.fix_eye_direction")
        
        
class VRMToRigifyMetarigUtilitiesPanel(bpy.types.Panel):
    """"""
    bl_label = "Utilities"
    bl_idname = "VRM_TO_RIGIFY_METARIG_PT_utilities_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRM To Rigify Metarig"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.operator("vrm_to_rigify_metarig.enable_all_ik_stretch")
        col.operator("vrm_to_rigify_metarig.disable_all_ik_stretch")
        
        col = layout.column(align=True)
        col.operator("vrm_to_rigify_metarig.hide_toon_shader")
        col.operator("vrm_to_rigify_metarig.show_toon_shader")
        
        col = layout.column(align=True)
        col.operator("vrm_to_rigify_metarig.recalibrate_eye_direction")
        
        col = layout.column(align=True)
        col.operator("vrm_to_rigify_metarig.look_at_object_constraint")
        col.operator("vrm_to_rigify_metarig.clear_look_at_constraint")
        
        col = layout.column(align=True)
        col.operator("vrm_to_rigify_metarig.show_default_visible_layers")
        col.operator("vrm_to_rigify_metarig.show_all_control_layers")


CLASSES = [
    ShowDefaultVisibleLayers,
    ShowAllControlLayers,
    RemoveUnusedBones,
    AlignHeadBone,
    AlignHandBones,
    AlignFeetBones,
    EnableAllIKStretch,
    DisableAllIKStretch,
    FixEyeDirection,
    RecalibrateEyeDirection,
    HideToonShaderInViewport,
    ShowToonShaderInViewport,
    LookAtObjectConstraint,
    ClearLookAtConstraint,
    VRMToRigifyMetarigMainPanel,
    VRMToRigifyMetarigOperatorsPanel,
    VRMToRigifyMetarigUtilitiesPanel,
    GenerateMetarig,
    OneClickSetup,
    Regenerate
]


def register():
    for clazz in CLASSES:
        bpy.utils.register_class(clazz)


def unregister():
    for clazz in CLASSES:
        bpy.utils.unregister_class(clazz)


if __name__ == "__main__":
    register()
