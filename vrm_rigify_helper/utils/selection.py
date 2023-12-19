import bpy

from ..common import bone_select_set
from ..checks import is_rigify_rig


def select_all_root_bones(context):
    initial_mode = context.view_layer.objects.active.mode
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.armature.select_all(action='SELECT')
    
    bones = context.selected_editable_bones
    
    for bone in bones:
        if bone.parent:  # if the bone has parent (it is a child bone)
            bone_select_set(bone, False)
            
    if initial_mode == 'OBJECT':
        bpy.ops.object.mode_set(mode='POSE')
    else:
        bpy.ops.object.mode_set(mode=initial_mode)
        
        
def select_root_bones(context, tag):
    initial_mode = context.view_layer.objects.active.mode

    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.armature.select_all(action='SELECT')
    
    bones = context.selected_editable_bones
    
    for bone in bones:
        # If bone has parent and parent's tag is the same (is tail) => deselect
        # bone is not tagged  => deselect
        if (bone.parent and bone.parent.get('extracted_vrm_bone') == tag) or (bone.get('extracted_vrm_bone') != tag):
            bone_select_set(bone, False)
            
    if initial_mode == 'OBJECT':
        bpy.ops.object.mode_set(mode='EDIT')
    else:
        bpy.ops.object.mode_set(mode=initial_mode)


class BaseSelector(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return (obj and obj.data and obj.type == 'ARMATURE' and 'rig_id' not in obj.data)


class SelectAllRootBones(BaseSelector):
    """Tooltip"""
    bl_idname = "vrm_rigify_helper.select_all_root_bones"
    bl_label = "Select All Root Bones"

    def execute(self, context):
        select_all_root_bones(context)
        return {'FINISHED'}
        
        
class SelectHairRootBones(BaseSelector):
    """Tooltip"""
    bl_idname = "vrm_rigify_helper.select_hair_root_bones"
    bl_label = "Select Hair Root Bones"

    def execute(self, context):
        select_root_bones(context, 'hair')
        return {'FINISHED'}
        
        
class SelectSkirtRootBones(BaseSelector):
    """Tooltip"""
    bl_idname = "vrm_rigify_helper.select_skirt_root_bones"
    bl_label = "Select Skirt Root Bones"

    def execute(self, context):
        select_root_bones(context, 'skirt')
        return {'FINISHED'}
        
        
class SelectCoatSkirtRootBones(BaseSelector):
    """Tooltip"""
    bl_idname = "vrm_rigify_helper.select_coat_skirt_root_bones"
    bl_label = "Select Coat Skirt Root Bones"

    def execute(self, context):
        select_root_bones(context, 'coat_skirt')
        return {'FINISHED'}
