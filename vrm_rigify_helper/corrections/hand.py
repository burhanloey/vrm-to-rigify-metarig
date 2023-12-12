import bpy

from math import radians
from ..checks import is_metarig


def set_bone_rolls(rig, bone_names, roll_in_degree):
    for name in bone_names:
        edit_bone = rig.data.edit_bones.get(name)
        
        if edit_bone:
            edit_bone.roll = radians(roll_in_degree)


def set_bone_length(rig, bone_name, new_length):
    bone = rig.data.edit_bones.get(bone_name)
    
    if bone:
        bone.length = new_length


def select_bone(bone):
    bone.select = True
    bone.select_head = True
    bone.select_tail = True
    
    
def deselect_bone(bone):
    bone.select = False
    bone.select_head = False
    bone.select_tail = False


def set_bend_rotation_axis(rig, main_bone_names, side, axis):
    for name in main_bone_names:
        rig.pose.bones.get(name + '.01.' + side).rigify_parameters.primary_rotation_axis = axis


def align_fingers(rig, main_bone_names, side, bend_angle_in_degree):
    for name in main_bone_names:
        bpy.ops.armature.select_all(action='DESELECT')
    
        main_bone = rig.data.edit_bones.get(name + '.01.' + side)
        second_bone = rig.data.edit_bones.get(name + '.02.' + side)
        third_bone = rig.data.edit_bones.get(name + '.03.' + side)
        
        select_bone(main_bone)
        rig.data.edit_bones.active = main_bone
        
        bpy.ops.armature.select_linked()
        bpy.ops.armature.align()
        
        deselect_bone(main_bone)
        select_bone(second_bone)
        select_bone(third_bone)
        
        bpy.ops.transform.rotate(value=radians(-bend_angle_in_degree), orient_axis='Z', orient_type='NORMAL', center_override=main_bone.tail)
        
        deselect_bone(second_bone)
        
        bpy.ops.transform.rotate(value=radians(-bend_angle_in_degree), orient_axis='Z', orient_type='NORMAL', center_override=second_bone.tail)


def align_hand_bones(context):
    metarig = context.view_layer.objects.active
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    initial_mirror_setting = metarig.data.use_mirror_x
    
    metarig.data.use_mirror_x = True
    
    set_bone_rolls(metarig, ['upper_arm.L', 'forearm.L', 'hand.L'], 90.0)
    set_bone_length(metarig, 'hand.L', 0.06)
    
    set_bone_rolls(metarig, ['f_index.01.L', 'f_middle.01.L', 'f_ring.01.L', 'f_pinky.01.L'], -90.0)
    align_fingers(metarig, ['thumb', 'f_index', 'f_middle', 'f_ring', 'f_pinky'], 'L', 5.0)
    
    set_bend_rotation_axis(metarig, ['thumb', 'f_index', 'f_middle', 'f_ring', 'f_pinky'], 'L', 'automatic')
    set_bend_rotation_axis(metarig, ['thumb', 'f_index', 'f_middle', 'f_ring', 'f_pinky'], 'R', 'automatic')
    
    # Reset to initial settings
    metarig.data.use_mirror_x = initial_mirror_setting
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    metarig.show_in_front = True


class AlignHandBones(bpy.types.Operator):
    """Align hand bone to cover the whole palm. Fix the arm bone rolls. Bend the fingers towards proper direction"""
    bl_idname = "vrm_rigify_helper.align_hand_bones"
    bl_label = "Align Hand Bones"

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        align_hand_bones(context)
        return {'FINISHED'}
