import bpy

from ..checks import is_metarig
from ..common import bmesh_editing, symmetrical_editing, switch_active_object, find_body_mesh_object, select_only_vertex_group


def align_head_bone(context):
    metarig = context.view_layer.objects.active
    vrm_rig = metarig['vrm_rig']
    
    switch_active_object(context, vrm_rig)
    bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
    
    body_mesh = find_body_mesh_object(context.selected_objects)
    
    switch_active_object(context, body_mesh)
    bpy.ops.object.mode_set(mode='EDIT')
    select_only_vertex_group('DEF-spine.006')  # head vertex group
    
    with bmesh_editing(body_mesh) as bm:
        selected_verts = list(filter(lambda v: v.select, bm.verts))
        any_vert_global_pos = selected_verts[0].co @ body_mesh.matrix_world
        
        head_top_z = any_vert_global_pos.z
        
        for v in selected_verts:
            v_global_pos = v.co @ body_mesh.matrix_world
            
            if v_global_pos.z > head_top_z:
                head_top_z = v_global_pos.z
    
        switch_active_object(context, metarig)
        bpy.ops.object.mode_set(mode='EDIT')
        
        with symmetrical_editing(metarig):
            head_bone = metarig.data.edit_bones.get('spine.006')
            head_bone.tail.x = 0.0
            head_bone.tail.y = head_bone.head.y  # make it straight upward
            head_bone.tail.z = head_top_z


class AlignHeadBone(bpy.types.Operator):
    """Align head bone vertically"""
    bl_idname = "vrm_rigify_helper.align_head_bone"
    bl_label = "Align Head Bone"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        align_head_bone(context)
        return {'FINISHED'}
