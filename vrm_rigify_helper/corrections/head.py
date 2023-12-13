import bpy

from ..checks import is_metarig


def align_head_bone(context):
    metarig = context.view_layer.objects.active
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    head_bone = metarig.data.edit_bones.get('spine.006')
    
    if not head_bone:
        return
    
    head_bone.tail.x = 0.0
    head_bone.tail.y = head_bone.head.y
    head_bone.length = 0.2
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    metarig.show_in_front = True


class AlignHeadBone(bpy.types.Operator):
    """Align head bone vertically"""
    bl_idname = "vrm_rigify_helper.align_head_bone"
    bl_label = "Align Head Bone"

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        align_head_bone(context)
        return {'FINISHED'}
