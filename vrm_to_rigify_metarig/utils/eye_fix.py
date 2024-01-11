import bpy
import mathutils

from ..checks import is_rigify_rig, is_face_mesh


def find_face_mesh_object(objs):
    for obj in objs:
        if is_face_mesh(obj):
            return obj
    return None


def has_face_mesh_object(objs):
    return bool(find_face_mesh_object(objs))


def find_eye_mesh_x_location(context, face_obj):
    context.view_layer.objects.active = face_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Select left eye vertex group
    eye_L_vg = face_obj.vertex_groups['DEF-eye.L']
    face_obj.vertex_groups.active = eye_L_vg
    bpy.ops.object.vertex_group_select()
    
    bpy.ops.view3d.snap_cursor_to_selected()
    
    # Get location from empty object
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.empty_add()
    
    new_empty = context.view_layer.objects.active
    x_location = new_empty.location.x
    
    bpy.ops.object.delete(use_global=True, confirm=False)
    
    bpy.ops.view3d.snap_cursor_to_center()

    return x_location
    
    
def find_eye_bone_x_location(context, rig):
    context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode='EDIT')
    
    return rig.data.edit_bones['MCH-eye.L'].head.x


def fix_eye_direction(context):
    rig = context.view_layer.objects.active
    face_obj = find_face_mesh_object(context.selected_editable_objects)
    eye_mesh_x = find_eye_mesh_x_location(context, face_obj)
    eye_bone_x = find_eye_bone_x_location(context, rig)
    
    adjustment_ratio = eye_bone_x / eye_mesh_x
    
    bpy.ops.object.mode_set(mode='POSE')
    
    rig.pose.bones['MCH-eye.L'].constraints['Damped Track'].influence = adjustment_ratio
    rig.pose.bones['MCH-eye.R'].constraints['Damped Track'].influence = adjustment_ratio
    
    bpy.ops.pose.select_all(action='DESELECT')
    rig.data.bones.active = rig.data.bones['eye_common']


class FixEyeDirection(bpy.types.Operator):
    """Fix eye direction to look at the control bone"""
    bl_idname = "vrm_to_rigify_metarig.fix_eye_direction"
    bl_label = "Fix Eye Direction"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active_obj = context.view_layer.objects.active
        if not is_rigify_rig(active_obj):
            return False
        
        objs = context.selected_editable_objects
        if not (objs and len(objs) == 2):
            return False
            
        return has_face_mesh_object(objs)

    def execute(self, context):
        fix_eye_direction(context)
        return {'FINISHED'}
