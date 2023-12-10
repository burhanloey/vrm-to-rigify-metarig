bl_info = {
    "name": "VRM Rigify Helper",
    "blender": (2, 80, 0),
    "category": "Rigging",
}

import bpy

from .extraction import ExtractVRMExtraBonesAsRigify
from .layers import UpdateMetarigBoneLayers
from .vertex_groups import RenameVRMVertexGroupsToRigify
from .cleanup import RemoveUnusedBones
from .wrapper import GenerateVRMMetaRigWrapper
from .mergers import MergeRigs
from .utils import SelectAllRootBones, SelectHairRootBones, SelectSkirtRootBones, SelectCoatSkirtRootBones


class VRMRigifyHelperSidebarPanel(bpy.types.Panel):
    """Utility operations to help with VRM Rigify addon"""
    bl_label = "VRM Rigify Helper"
    bl_idname = "VRM_RIGIFY_HELPER_PT_sidebar_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRM Rigify Helper"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        
        row = layout.row()
        row.operator("vrm_rigify_helper.generate_vrm_meta_rig")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.extract_vrm_extra_bones_as_rigify")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.update_metarig_bone_layers")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.merge_rigs")

        row = layout.row()
        row.operator("vrm_rigify_helper.rename_vrm_vertex_groups_to_rigify")
        
        row = layout.row()
        row.label(text="After generating Rigify rig:")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.remove_unused_bones")
        
        row = layout.row()
        row.label(text="Utilities:")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.select_hair_root_bones")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.select_skirt_root_bones")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.select_coat_skirt_root_bones")
        
        row = layout.row()
        row.operator("vrm_rigify_helper.select_all_root_bones")


CLASSES = [
    ExtractVRMExtraBonesAsRigify,
    UpdateMetarigBoneLayers,
    RenameVRMVertexGroupsToRigify,
    RemoveUnusedBones,
    GenerateVRMMetaRigWrapper,
    MergeRigs,
    SelectAllRootBones,
    SelectHairRootBones,
    SelectSkirtRootBones,
    SelectCoatSkirtRootBones,
    VRMRigifyHelperSidebarPanel
]


def register():
    for clazz in CLASSES:
        bpy.utils.register_class(clazz)


def unregister():
    for clazz in CLASSES:
        bpy.utils.unregister_class(clazz)


if __name__ == "__main__":
    register()
