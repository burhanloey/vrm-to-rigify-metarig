import bpy
import bmesh

from ..checks import is_metarig, is_body_mesh


def select_only_vertex_group(group_name):
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=group_name)
    bpy.ops.object.vertex_group_select()


class BMeshEditing:
    def __init__(self, mesh_obj):
        self.mesh_obj = mesh_obj
    def __enter__(self):
        self.bm = bmesh.from_edit_mesh(self.mesh_obj.data)
        self.bm.faces.active = None
        return self.bm
    def __exit__(self, _type, _value, _trace):
        self.bm.free()


def bmesh_editing(mesh_obj):
    return BMeshEditing(mesh_obj)


class Symmetry:
    def __init__(self, obj):
        self.obj = obj
    def __enter__(self):
        self.initial_setting = self.obj.data.use_mirror_x
        self.obj.data.use_mirror_x = True
    def __exit__(self, _type, _value, _trace):
        if self.obj.data.use_mirror_x != self.initial_setting:
            self.obj.data.use_mirror_x = self.initial_setting


def symmetry(obj):
    return Symmetry(obj)


def switch_active_object(context, obj):
    current_mode = context.view_layer.objects.active.mode
    if current_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    context.view_layer.objects.active = obj
    obj.select_set(True)


def find_body_mesh_object(objs):
    for obj in objs:
        if is_body_mesh(obj):
            return obj
    return None


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
        
        with symmetry(metarig):
            heel_bone = metarig.data.edit_bones.get('heel.02.L')
            heel_bone.head.x = heel_head_x
            heel_bone.head.y = heel_y
            heel_bone.tail.x = heel_tail_x
            heel_bone.tail.y = heel_y


def align_toe_bones(context, metarig, body_mesh):
    switch_active_object(context, body_mesh)
    bpy.ops.object.mode_set(mode='EDIT')
    select_only_vertex_group('DEF-foot.L')
    
    bm = bmesh.from_edit_mesh(body_mesh.data)
    bm.faces.active = None
    
    selected_verts = list(filter(lambda v: v.select, bm.verts))
    any_vert_global_pos = selected_verts[0].co @ body_mesh.matrix_world
    
    foot_front_y = any_vert_global_pos.y
    
    for v in selected_verts:
        v_global_pos = v.co @ body_mesh.matrix_world
        
        if v_global_pos.y < foot_front_y:  # -ve is towards front
            foot_front_y = v_global_pos.y
    
    bm.free()
    
    select_only_vertex_group('DEF-toe.L')
    
    bm = bmesh.from_edit_mesh(body_mesh.data)
    bm.faces.active = None
    
    selected_verts = list(filter(lambda v: v.select, bm.verts))
    any_vert_global_pos = selected_verts[0].co @ body_mesh.matrix_world
    
    toe_base_y = any_vert_global_pos.y
    
    for v in selected_verts:
        v_global_pos = v.co @ body_mesh.matrix_world
        
        if v_global_pos.y > toe_base_y:  # -ve is towards front
            toe_base_y = v_global_pos.y
    
    bm.free()
    
    toe_head_y = (foot_front_y + toe_base_y) / 2
    
    switch_active_object(context, metarig)
    bpy.ops.object.mode_set(mode='EDIT')
    
    initial_mirror_setting = metarig.data.use_mirror_x
    metarig.data.use_mirror_x = True
    
    toe_bone = metarig.data.edit_bones.get('toe.L')
    toe_bone.head.y = toe_head_y


def align_feet_bones(context):
    metarig = context.view_layer.objects.active
    vrm_rig = metarig['vrm_rig']
    
    switch_active_object(context, vrm_rig)
    bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
    body_mesh = find_body_mesh_object(context.selected_objects)
    
    align_heel_bones(context, metarig, body_mesh)
    align_toe_bones(context, metarig, body_mesh)
    
    # TODO: do the same for these
    toe_y = 0.0
    toe_z = 0.0
    toe_end_y = 0.0
    toe_end_z = 0.0
    
    # TODO: align toe bones relative to the mesh
    
    
    
    commented_out = """
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
    """
    
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
