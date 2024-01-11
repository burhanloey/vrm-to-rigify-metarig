import bpy

from ..checks import is_metarig, is_body_mesh
from ..common import bmesh_editing, symmetrical_editing, switch_active_object, find_body_mesh_object, select_only_vertex_group


def align_heel_bones(context, metarig, body_mesh):
    switch_active_object(context, body_mesh)
    bpy.ops.object.mode_set(mode='EDIT')
    select_only_vertex_group('DEF-foot.L')
    
    with bmesh_editing(body_mesh) as bm:
        selected_verts = list(filter(lambda v: v.select, bm.verts))
        any_vert_global_pos = selected_verts[0].co @ body_mesh.matrix_world
    
        heel_y = any_vert_global_pos.y
        heel_tail_x = any_vert_global_pos.x
        heel_head_x = any_vert_global_pos.x
        
        for v in selected_verts:
            v_global_pos = v.co @ body_mesh.matrix_world
        
            if v_global_pos.y > heel_y:
                heel_y = v_global_pos.y
            if v_global_pos.x < heel_head_x:
                heel_head_x = v_global_pos.x
            if v_global_pos.x > heel_tail_x:
                heel_tail_x = v_global_pos.x
        
        switch_active_object(context, metarig)
        bpy.ops.object.mode_set(mode='EDIT')
        
        with symmetrical_editing(metarig):
            heel_bone = metarig.data.edit_bones.get('heel.02.L')
            heel_bone.head.x = heel_head_x
            heel_bone.head.y = heel_y
            heel_bone.tail.x = heel_tail_x
            heel_bone.tail.y = heel_y


def align_toe_bones(context, metarig, body_mesh):
    switch_active_object(context, body_mesh)
    bpy.ops.object.mode_set(mode='EDIT')
    select_only_vertex_group('DEF-toe.L')
    
    with bmesh_editing(body_mesh) as bm:
        selected_verts = list(filter(lambda v: v.select, bm.verts))
        any_vert_global_pos = selected_verts[0].co @ body_mesh.matrix_world
        
        toe_front_y = any_vert_global_pos.y
        
        for v in selected_verts:
            v_global_pos = v.co @ body_mesh.matrix_world
            
            if v_global_pos.y < toe_front_y:  # -ve is towards front
                toe_front_y = v_global_pos.y
    
        switch_active_object(context, metarig)
        bpy.ops.object.mode_set(mode='EDIT')
        
        with symmetrical_editing(metarig):
            toe_bone = metarig.data.edit_bones.get('toe.L')
            toe_bone.tail.y = toe_front_y
            toe_bone.tail.z = toe_bone.head.z


def align_feet_bones(context):
    metarig = context.view_layer.objects.active
    vrm_rig = metarig['vrm_rig']
    
    switch_active_object(context, vrm_rig)
    bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
    body_mesh = find_body_mesh_object(context.selected_objects)
    
    align_heel_bones(context, metarig, body_mesh)
    align_toe_bones(context, metarig, body_mesh)
    
    bpy.ops.object.mode_set(mode='OBJECT')


class AlignFeetBones(bpy.types.Operator):
    """Align feet bones"""
    bl_idname = "vrm_rigify_helper.align_feet_bones"
    bl_label = "Align Feet Bones"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        align_feet_bones(context)
        return {'FINISHED'}
