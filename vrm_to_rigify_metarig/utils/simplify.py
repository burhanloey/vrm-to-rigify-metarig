import bpy

from ..checks import is_metarig
from ..metarig import BONE_MAPPING, FINGER_BONE_NAMES


def get_required_bones(include_fingers):
    if include_fingers:
        return [b for b in BONE_MAPPING.values() if 'eye' not in b]
    else:
        return [b for b in BONE_MAPPING.values() if 'eye' not in b and b not in FINGER_BONE_NAMES]


def extract_basic_skeleton(context, include_fingers=False):
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.duplicate()
    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.armature.select_all(action='SELECT')
    
    required_bones = get_required_bones(include_fingers)
    
    # Deselect required bones and delete the selected
    for bone in context.selected_editable_bones:
        if bone.name in required_bones:
            bone.select = False
            bone.select_head = False
            bone.select_tail = False
    
    bpy.ops.armature.delete(confirm=False)
    
    bpy.ops.object.mode_set(mode='OBJECT')


class BaseExtractBasicSkeleton(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)


class ExtractBasicSkeleton(BaseExtractBasicSkeleton):
    """Extract simplified version of the metarig to be used by another plugin, for e.g. Expy Kit"""
    bl_idname = "vrm_to_rigify_metarig.extract_basic_skeleton"
    bl_label = "Extract Basic Skeleton"

    def execute(self, context):
        extract_basic_skeleton(context)
        return {'FINISHED'}


class ExtractBasicSkeletonWithFingers(BaseExtractBasicSkeleton):
    """Extract simplified version of the metarig including finger bones"""
    bl_idname = "vrm_to_rigify_metarig.extract_basic_skeleton_with_fingers"
    bl_label = "Extract Basic Skeleton with Fingers"

    def execute(self, context):
        extract_basic_skeleton(context, include_fingers=True)
        return {'FINISHED'}