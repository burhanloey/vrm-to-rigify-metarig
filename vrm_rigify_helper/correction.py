import bpy
import mathutils

from .checks import is_metarig


FACIAL_BONES = [
    'face',
    'nose',
    'nose.001',
    'nose.002',
    'nose.003',
    'nose.004',
    'lip.T.L',
    'lip.T.L.001',
    'lip.B.L',
    'lip.B.L.001',
    'jaw',
    'chin',
    'chin.001',
    'ear.L',
    'ear.L.001',
    'ear.L.002',
    'ear.L.003',
    'ear.L.004',
    'ear.R',
    'ear.R.001',
    'ear.R.002',
    'ear.R.003',
    'ear.R.004',
    'lip.T.R',
    'lip.T.R.001',
    'lip.B.R',
    'lip.B.R.001',
    'brow.B.L',
    'brow.B.L.001',
    'brow.B.L.002',
    'brow.B.L.003',
    'lid.T.L',
    'lid.T.L.001',
    'lid.T.L.002',
    'lid.T.L.003',
    'lid.B.L',
    'lid.B.L.001',
    'lid.B.L.002',
    'lid.B.L.003',
    'brow.B.R',
    'brow.B.R.001',
    'brow.B.R.002',
    'brow.B.R.003',
    'lid.T.R',
    'lid.T.R.001',
    'lid.T.R.002',
    'lid.T.R.003',
    'lid.B.R',
    'lid.B.R.001',
    'lid.B.R.002',
    'lid.B.R.003',
    'forehead.L',
    'forehead.L.001',
    'forehead.L.002',
    'temple.L',
    'jaw.L',
    'jaw.L.001',
    'chin.L',
    'cheek.B.L',
    'cheek.B.L.001',
    'brow.T.L',
    'brow.T.L.001',
    'brow.T.L.002',
    'brow.T.L.003',
    'forehead.R',
    'forehead.R.001',
    'forehead.R.002',
    'temple.R',
    'jaw.R',
    'jaw.R.001',
    'chin.R',
    'cheek.B.R',
    'cheek.B.R.001',
    'brow.T.R',
    'brow.T.R.001',
    'brow.T.R.002',
    'brow.T.R.003',
    'cheek.T.L',
    'cheek.T.L.001',
    'nose.L',
    'nose.L.001',
    'cheek.T.R',
    'cheek.T.R.001',
    'nose.R',
    'nose.R.001',
    'teeth.T',
    'teeth.B',
    'tongue',
    'tongue.001',
    'tongue.002'
]


def select_bone(rig, bone_name):
    bone = rig.data.edit_bones.get(bone_name)

    if bone:
        bone.select = True
        bone.select_head = True
        bone.select_tail = True


def align_facial_bones(context):
    metarig = bpy.context.view_layer.objects.active

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    
    select_bone(metarig, 'eye.L')
    select_bone(metarig, 'eye.R')

    bpy.ops.view3d.snap_cursor_to_selected()
    
    bpy.ops.armature.select_all(action='DESELECT')
    
    for bone in FACIAL_BONES:
        select_bone(metarig, bone)
        
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
    
    # Resize and position the facial bones
    initial_pivot = bpy.context.scene.tool_settings.transform_pivot_point
    
    bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
    
    bpy.ops.transform.resize(value=mathutils.Vector((0.32, 0.32, 0.32)))
    bpy.ops.transform.translate(value=mathutils.Vector((0.0, 0.0, -0.008)))
    
    bpy.context.scene.tool_settings.transform_pivot_point = initial_pivot
    
    bpy.ops.view3d.snap_cursor_to_center()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    metarig.show_in_front = True


class AlignFacialBones(bpy.types.Operator):
    """Align facial bones to the eye bones. Does not align to mesh. This is required to generate Rigify rig using upgraded face rig"""
    bl_idname = "vrm_rigify_helper.align_facial_bones"
    bl_label = "Align Facial Bones"

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        align_facial_bones(context)
        return {'FINISHED'}
