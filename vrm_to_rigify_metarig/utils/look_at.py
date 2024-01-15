import bpy

from ..checks import is_rigify_rig


def look_at_object_constraint(context):
    bpy.ops.object.mode_set(mode='OBJECT')

    rig = context.view_layer.objects.active

    def get_other_selection(objs):
        for obj in objs:
            if obj is not rig:
                return obj
        return None

    target = get_other_selection(context.selected_objects)
    
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    rig.data.bones.active = rig.data.bones['eye_common']
    
    eye_ctrl_pose_bone = rig.pose.bones['eye_common']
    
    # Damped track constraint
    bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
    
    eye_ctrl_pose_bone.constraints['Damped Track'].target = target
    eye_ctrl_pose_bone.constraints['Damped Track'].track_axis = 'TRACK_Z'
    
    # Copy location constraint
    bpy.ops.pose.constraint_add(type='COPY_LOCATION')
    
    eye_ctrl_pose_bone.constraints['Copy Location'].target = target


def clear_look_at_constraint(context):
    rig = context.view_layer.objects.active
    
    bpy.ops.object.mode_set(mode='POSE')
    rig.data.bones.active = rig.data.bones['eye_common']
    
    if rig.pose.bones['eye_common'].constraints.get('Damped Track'):
        bpy.ops.constraint.delete(constraint='Damped Track', owner='BONE')
    if rig.pose.bones['eye_common'].constraints.get('Copy Location'):
        bpy.ops.constraint.delete(constraint='Copy Location', owner='BONE')


class LookAtObjectConstraint(bpy.types.Operator):
    """Make the character look at the selected object using constraints.
    
Select both the rig and the object to look at. Set the rig as active. The constraints will be set up at the 'eye_common' bone"""
    bl_idname = "vrm_to_rigify_metarig.look_at_object_constraint"
    bl_label = "Look At Object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        objs = context.selected_objects
        active_obj = context.view_layer.objects.active
        return len(objs) == 2 and is_rigify_rig(active_obj)

    def execute(self, context):
        look_at_object_constraint(context)
        return {'FINISHED'}


class ClearLookAtConstraint(bpy.types.Operator):
    """Clear the look at constraint"""
    bl_idname = "vrm_to_rigify_metarig.clear_look_at_constraint"
    bl_label = "Clear Look At Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_rigify_rig(obj)

    def execute(self, context):
        clear_look_at_constraint(context)
        return {'FINISHED'}
