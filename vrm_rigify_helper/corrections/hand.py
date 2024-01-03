import bpy

from math import radians
from ..checks import is_metarig
from ..common import bone_select_set


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
    bone_select_set(bone, True)
    
    
def deselect_bone(bone):
    bone_select_set(bone, False)


def set_bend_rotation_axis(rig, main_bone_names, side, axis):
    for name in main_bone_names:
        rig.pose.bones.get(name + '.01.' + side).rigify_parameters.primary_rotation_axis = axis


def bend_fingers(rig, main_bone_names, side, bend_angle_in_degree, axis):
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
        
        bpy.ops.transform.rotate(value=radians(bend_angle_in_degree), orient_axis=axis, orient_type='NORMAL', center_override=main_bone.tail)
        
        deselect_bone(second_bone)
        
        bpy.ops.transform.rotate(value=radians(bend_angle_in_degree), orient_axis=axis, orient_type='NORMAL', center_override=second_bone.tail)


def find_closest_bone_from_hand(metarig):
    closest_bone = metarig.data.edit_bones.get('f_index.01.L')
    
    for name in ['f_middle.01.L', 'f_ring.01.L', 'f_pinky.01.L']:
        bone = metarig.data.edit_bones.get(name)
        
        if bone.head.x < closest_bone.head.x:
            closest_bone = bone
    
    return closest_bone


def lengthen_hand_bone(metarig):
    closest_bone = find_closest_bone_from_hand(metarig)
    
    hand_bone = metarig.data.edit_bones.get('hand.L')
    
    x = hand_bone.tail.x - hand_bone.head.x
    z = hand_bone.tail.z - hand_bone.head.z
    x_target = closest_bone.head.x - hand_bone.head.x
    
    z_target = z * (x_target / x)  # magnification ratio
    
    hand_bone.tail.x = hand_bone.head.x + x_target
    hand_bone.tail.z = hand_bone.head.z + z_target


def align_hand_bones(context):
    metarig = context.view_layer.objects.active
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    initial_mirror_setting = metarig.data.use_mirror_x
    
    metarig.data.use_mirror_x = True
    
    lengthen_hand_bone(metarig)
    
    bend_fingers(metarig, ['f_index', 'f_middle', 'f_ring', 'f_pinky'], 'L', 5.0, 'X')
    bend_fingers(metarig, ['thumb'], 'L', -5.0, 'Z')
    
    # Reset to initial settings
    metarig.data.use_mirror_x = initial_mirror_setting
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    metarig.show_in_front = True


class AlignHandBones(bpy.types.Operator):
    """Align hand bone to cover the whole palm. Fix the arm bone rolls. Bend the fingers towards proper direction"""
    bl_idname = "vrm_rigify_helper.align_hand_bones"
    bl_label = "Align Hand Bones"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        align_hand_bones(context)
        return {'FINISHED'}
