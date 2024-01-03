bl_info = {
    "name": "VRM Rigify Helper",
    "author": "burhanloey",
    "description": "Helper addon for vrm-rigify",
    "version": (0, 1, 1),
    "blender": (2, 80, 0),
    "location": "3D Viewport > VRM Rigify Helper Panel",
    "doc_url": "https://github.com/burhanloey/vrm-rigify-helper",
    "tracker_url": "https://github.com/burhanloey/vrm-rigify-helper/issues",
    "category": "Rigging",
}

import bpy

from .extraction import ExtractVRMExtraBonesAsRigify
from .layers import UpdateMetarigBoneLayers, ShowDefaultVisibleLayers, ShowAllControlLayers
from .vertex_groups import RenameVRMVertexGroupsToRigify
from .cleanup import RemoveUnusedBones
from .wrapper import GenerateVRMMetaRigWrapper
from .mergers import MergeRigs
from .corrections.facial import AlignFacialBones
from .corrections.head import AlignHeadBone
from .corrections.hand import AlignHandBones
from .corrections.feet import AlignFeetBones
from .utils.selection import SelectAllRootBones, SelectHairRootBones, SelectSkirtRootBones, SelectCoatSkirtRootBones
from .utils.extra_bones import EnableHairFollow, DisableHairFollow, EnableClothFollow, DisableClothFollow, EnableAllIKStretch, DisableAllIKStretch
from .utils.eye_fix import FixEyeDirection
from .metarig import GenerateMetarig
from .main import OneClickSetup, Regenerate

from .checks import is_vrm_rig, is_metarig, is_rigify_rig


def has_target_rig(obj):
    return bool(obj.data.rigify_target_rig)


class VRMRigifyHelperMainPanel(bpy.types.Panel):
    """Utility operations to help with VRM Rigify addon"""
    bl_label = "VRM Rigify Helper"
    bl_idname = "VRM_RIGIFY_HELPER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRM Rigify Helper"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.scale_y = 2.0
        
        obj = context.view_layer.objects.active
        
        if is_metarig(obj) and has_target_rig(obj):
            row.operator("vrm_rigify_helper.regenerate", icon="OUTLINER_OB_ARMATURE")
        else:
            row.operator("vrm_rigify_helper.one_click_setup", icon="OUTLINER_OB_ARMATURE")


class VRMRigifyHelperOperatorsPanel(bpy.types.Panel):
    """"""
    bl_label = "Operators"
    bl_idname = "VRM_RIGIFY_HELPER_PT_operators_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRM Rigify Helper"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("vrm_rigify_helper.generate_vrm_meta_rig")  # TODO: remove this
        row = layout.row()
        row.operator("vrm_rigify_helper.generate_metarig")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.update_metarig_bone_layers")
        
        row = layout.row()
        row.label(text="Bone alignment:")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.align_facial_bones", text="Facial")
        row.operator("vrm_rigify_helper.align_head_bone", text="Head")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.align_hand_bones", text="Hand")
        row.operator("vrm_rigify_helper.align_feet_bones", text="Feet")
        
        row = layout.separator()
        
        row = layout.row()
        row.operator("vrm_rigify_helper.extract_vrm_extra_bones_as_rigify")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.merge_rigs")
        
        row = layout.separator()

        row = layout.row()
        row.operator("vrm_rigify_helper.rename_vrm_vertex_groups_to_rigify")
        
        row = layout.separator()
        
        row = layout.row()
        row.operator("vrm_rigify_helper.remove_unused_bones")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.fix_eye_direction")
        
        
class VRMRigifyHelperUtilitiesPanel(bpy.types.Panel):
    """"""
    bl_label = "Utilities"
    bl_idname = "VRM_RIGIFY_HELPER_PT_utilities_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRM Rigify Helper"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("vrm_rigify_helper.select_hair_root_bones")
        row = layout.row()
        row.operator("vrm_rigify_helper.select_skirt_root_bones")
        row = layout.row()
        row.operator("vrm_rigify_helper.select_coat_skirt_root_bones")
        
        row = layout.separator()
        
        row = layout.row()
        row.operator("vrm_rigify_helper.enable_hair_follow")
        row = layout.row()
        row.operator("vrm_rigify_helper.disable_hair_follow")
        
        row = layout.separator()
        
        row = layout.row()
        row.operator("vrm_rigify_helper.enable_cloth_follow")
        row = layout.row()
        row.operator("vrm_rigify_helper.disable_cloth_follow")
        
        row = layout.separator()
        
        row = layout.row()
        row.operator("vrm_rigify_helper.enable_all_ik_stretch")
        row = layout.row()
        row.operator("vrm_rigify_helper.disable_all_ik_stretch")
        
        row = layout.separator()
        
        row = layout.row()
        row.operator("vrm_rigify_helper.show_default_visible_layers")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.show_all_control_layers")


CLASSES = [
    ExtractVRMExtraBonesAsRigify,
    UpdateMetarigBoneLayers,
    ShowDefaultVisibleLayers,
    ShowAllControlLayers,
    RenameVRMVertexGroupsToRigify,
    RemoveUnusedBones,
    GenerateVRMMetaRigWrapper,
    MergeRigs,
    AlignFacialBones,
    AlignHeadBone,
    AlignHandBones,
    AlignFeetBones,
    SelectAllRootBones,
    SelectHairRootBones,
    SelectSkirtRootBones,
    SelectCoatSkirtRootBones,
    EnableHairFollow,
    DisableHairFollow,
    EnableClothFollow,
    DisableClothFollow,
    EnableAllIKStretch,
    DisableAllIKStretch,
    FixEyeDirection,
    VRMRigifyHelperMainPanel,
    VRMRigifyHelperOperatorsPanel,
    VRMRigifyHelperUtilitiesPanel,
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
