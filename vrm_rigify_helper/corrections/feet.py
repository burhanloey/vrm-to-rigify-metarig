import bpy

from ..checks import is_metarig


def align_feet_bones(context):
    metarig = context.view_layer.objects.active
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    initial_mirror_setting = metarig.data.use_mirror_x
    metarig.data.use_mirror_x = True
    
    foot_bone = metarig.data.edit_bones.get('foot.L')
    foot_bone.tail.z = 0.0167
    
    toe_bone = metarig.data.edit_bones.get('toe.L')
    toe_bone.tail.z = 0.0167
    toe_bone.length = 0.05
    
    heel_bone = metarig.data.edit_bones.get('heel.02.L')
    heel_bone.head.x = 0.042
    heel_bone.tail.x = 0.115
    heel_bone.head.y = heel_bone.tail.y = 0.072
    heel_bone.head.z = heel_bone.tail.z = 0
    
    metarig.data.use_mirror_x = initial_mirror_setting
    
    bpy.ops.object.mode_set(mode='OBJECT')


class AlignFeetBones(bpy.types.Operator):
    """Align feet bones"""
    bl_idname = "vrm_rigify_helper.align_feet_bones"
    bl_label = "Align Feet Bones"

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        align_feet_bones(context)
        return {'FINISHED'}