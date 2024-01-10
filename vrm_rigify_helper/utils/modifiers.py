import bpy

from ..checks import is_rigify_rig


def is_mesh(obj):
    return obj and obj.type == 'MESH'


def set_all_toon_modifiers(obj, is_visible):
    for modifier in obj.modifiers:
        if 'Toon' in modifier.name:
            modifier.show_viewport = is_visible


def set_toon_shader_visibility(context, is_visible):
    obj = context.view_layer.objects.active
    
    if is_mesh(obj):
        set_all_toon_modifiers(obj, is_visible)
    else:
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
        mesh_objs = filter(lambda obj: obj.type == 'MESH', context.selected_objects)
        
        for obj in mesh_objs:
            set_all_toon_modifiers(obj, is_visible)


class BaseToonShaderOperator(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_mesh(obj) or is_rigify_rig(obj)


class HideToonShaderInViewport(BaseToonShaderOperator):
    """Hide toon shader modifiers in viewport"""
    bl_idname = "vrm_rigify_helper.hide_toon_shader"
    bl_label = "Hide Toon Shader"

    def execute(self, context):
        set_toon_shader_visibility(context, is_visible=False)
        return {'FINISHED'}


class ShowToonShaderInViewport(BaseToonShaderOperator):
    """Make toon shader modifiers visible in viewport"""
    bl_idname = "vrm_rigify_helper.show_toon_shader"
    bl_label = "Show Toon Shader"

    def execute(self, context):
        set_toon_shader_visibility(context, is_visible=True)
        return {'FINISHED'}
