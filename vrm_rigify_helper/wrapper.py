import bpy

from .checks import is_vrm_rig


class GenerateVRMMetaRigWrapper(bpy.types.Operator):
    """Generate using vrm-rigify plugin"""
    bl_idname = "vrm_rigify_helper.generate_vrm_meta_rig"
    bl_label = "Generate VRM Meta-Rig"

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_vrm_rig(obj)

    def execute(self, context):
        bpy.ops.vrm_rigify.create_meta()
        return {'FINISHED'}
