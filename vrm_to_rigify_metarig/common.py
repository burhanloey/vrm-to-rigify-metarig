import bpy
import bmesh

from .checks import is_body_mesh


BLENDER_LAYER_COUNT = 32


def get_current_visible_layers(context):
    rig = context.view_layer.objects.active
    layer_count = len(rig.data.layers)
    
    current_visible_layers = [False] * layer_count
    
    for idx in range(layer_count):
        current_visible_layers[idx] = rig.data.layers[idx]
        
    return current_visible_layers
    
    
def layer_params(visible_layers=[]):
    params = [False] * BLENDER_LAYER_COUNT
    
    for layer in visible_layers:
        if 0 <= layer < BLENDER_LAYER_COUNT:
            params[layer] = True
            
    return params
    
    
def bone_select_set(bone, bool):
    bone.select = bool
    bone.select_head = bool
    bone.select_tail = bool


def select_only_vertex_group(group_name):
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group=group_name)
    bpy.ops.object.vertex_group_select()


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


class SymmetricalEditing:
    def __init__(self, obj):
        self.obj = obj
    def __enter__(self):
        self.initial_setting = self.obj.data.use_mirror_x
        self.obj.data.use_mirror_x = True
    def __exit__(self, _type, _value, _trace):
        if self.obj.data.use_mirror_x != self.initial_setting:
            self.obj.data.use_mirror_x = self.initial_setting


def symmetrical_editing(obj):
    return SymmetricalEditing(obj)
