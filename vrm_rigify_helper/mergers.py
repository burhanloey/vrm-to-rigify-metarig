import bpy

from .utils.selection import select_root_bones


def filter_bones(context, suffix):
    selected_bones = context.selected_editable_bones
    
    for bone in selected_bones:
        if bone.name and bone.name[-1] == suffix:
            continue
        
        bone.select = False
        bone.select_head = False
        bone.select_tail = False


def parent_selection(context, target_bone_full_name):
    metarig = context.view_layer.objects.active
    
    bpy.ops.object.select_pattern(pattern=target_bone_full_name)
    
    head_bone = context.selected_editable_bones[0]
    metarig.data.edit_bones.active = head_bone
    
    bpy.ops.armature.parent_set(type='OFFSET')

    
def parent_bones(context, tag, parent_bone, is_pair=False):
    if is_pair:
        select_root_bones(context, tag)
        filter_bones(context, 'L')
        parent_selection(context, parent_bone + '.L')
        
        select_root_bones(context, tag)
        filter_bones(context, 'R')
        parent_selection(context, parent_bone + '.R')
    else:
        select_root_bones(context, tag)
        parent_selection(context, parent_bone)


def merge_rigs(context):
    bpy.ops.object.join()
    
    parent_bones(context, 'hair', 'spine.006')
    parent_bones(context, 'skirt', 'thigh', is_pair=True)
    parent_bones(context, 'coat_skirt', 'shin', is_pair=True)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
class MergeRigs(bpy.types.Operator):
    """Make sure the metarig is the active object among the selection"""
    bl_idname = "vrm_rigify_helper.merge_rigs"
    bl_label = "Merge Rigs"

    @classmethod
    def poll(cls, context):
        objs = context.selected_editable_objects
        if not (objs and len(objs) > 1):
            return False
        for obj in context.selected_editable_objects:
            if obj.type != 'ARMATURE':
                return False
        return True

    def execute(self, context):
        merge_rigs(context)
        return {'FINISHED'}
