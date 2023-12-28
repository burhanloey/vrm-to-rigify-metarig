import bpy

from .checks import is_vrm_rig
from .common import layer_params, bone_select_set


# Mapping from vrm bone specification to rigify metarig bone name
# https://github.com/vrm-c/vrm-specification/tree/b5793b4ca250ed3acbde3dd7a47ee9ee1b3d60e9/specification/0.0#vrm-extension-models-bone-mapping-jsonextensionsvrmhumanoid
BONE_MAPPING = {
    # Torso
    "hips"      : "spine",
    "spine"     : "spine.001",
    "chest"     : "spine.002",
    "upperChest": "spine.003",
    "neck"      : "spine.004",

    # Head
    "head"    : "spine.006",
    "leftEye" : "eye.L",
    "rightEye": "eye.R",
    "jaw"     : "jaw",  # ignore

    # Leg
    "leftUpperLeg" : "thigh.L",
    "leftLowerLeg" : "shin.L",
    "leftFoot"     : "foot.L",
    "leftToes"     : "toe.L",
    "rightUpperLeg": "thigh.R",
    "rightLowerLeg": "shin.R",
    "rightFoot"    : "foot.R",
    "rightToes"    : "toe.R",

    # Arm
    "leftShoulder" : "shoulder.L",
    "leftUpperArm" : "upper_arm.L",
    "leftLowerArm" : "forearm.L",
    "leftHand"     : "hand.L",
    "rightShoulder": "shoulder.R",
    "rightUpperArm": "upper_arm.R",
    "rightLowerArm": "forearm.R",
    "rightHand"    : "hand.R",

    # Finger
    "leftThumbProximal"      : "thumb.01.L",
    "leftThumbIntermediate"  : "thumb.02.L",
    "leftThumbDistal"        : "thumb.03.L",
    "leftIndexProximal"      : "f_index.01.L",
    "leftIndexIntermediate"  : "f_index.02.L",
    "leftIndexDistal"        : "f_index.03.L",
    "leftMiddleProximal"     : "f_middle.01.L",
    "leftMiddleIntermediate" : "f_middle.02.L",
    "leftMiddleDistal"       : "f_middle.03.L",
    "leftRingProximal"       : "f_ring.01.L",
    "leftRingIntermediate"   : "f_ring.02.L",
    "leftRingDistal"         : "f_ring.03.L",
    "leftLittleProximal"     : "f_pinky.01.L",
    "leftLittleIntermediate" : "f_pinky.02.L",
    "leftLittleDistal"       : "f_pinky.03.L",
    "rightThumbProximal"     : "thumb.01.R",
    "rightThumbIntermediate" : "thumb.02.R",
    "rightThumbDistal"       : "thumb.03.R",
    "rightIndexProximal"     : "f_index.01.R",
    "rightIndexIntermediate" : "f_index.02.R",
    "rightIndexDistal"       : "f_index.03.R",
    "rightMiddleProximal"    : "f_middle.01.R",
    "rightMiddleIntermediate": "f_middle.02.R",
    "rightMiddleDistal"      : "f_middle.03.R",
    "rightRingProximal"      : "f_ring.01.R",
    "rightRingIntermediate"  : "f_ring.02.R",
    "rightRingDistal"        : "f_ring.03.R",
    "rightLittleProximal"    : "f_pinky.01.R",
    "rightLittleIntermediate": "f_pinky.02.R",
    "rightLittleDistal"      : "f_pinky.03.R",
}

UNNEEDED_BONES = ["Root"]


def find_bust_bone_names(metarig):
    bust_bone_names = []
    
    bone_groups = metarig.data.vrm_addon_extension.vrm0.secondary_animation.bone_groups
    
    for bone_group in bone_groups:
        if bone_group.comment != 'Bust':
            continue
        for bone in bone_group.bones:
            bust_bone_names.append(bone.bone_name)
        break  # there should be only one bust bone group, so short circuit the loop
    
    return bust_bone_names


def rename_bones(metarig):
    bpy.ops.object.mode_set(mode='EDIT')
    
    human_bones = metarig.data.vrm_addon_extension.vrm0.humanoid.human_bones
    
    for human_bone in human_bones:
        bone_name = human_bone.node.bone_name
        bone_spec = human_bone.bone
        
        if bone_spec not in BONE_MAPPING:
            continue
        
        bone = metarig.data.bones.get(bone_name)
            
        if bone:
            bone.name = BONE_MAPPING[bone_spec]


def remove_unneeded_bones(metarig):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    
    for unneeded_bone in UNNEEDED_BONES:
        bone = metarig.data.edit_bones.get(unneeded_bone)
        
        if bone:
            bone_select_set(bone, True)
            bpy.ops.armature.delete(confirm=False)


def detach_bone_from_parent(metarig, bone_name):
    bpy.ops.object.mode_set(mode='EDIT')
    
    bone = metarig.data.edit_bones[bone_name]
    
    if bone:
        bone.use_connect = False


def add_heel_bones(metarig):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.metarig_sample_add(metarig_type='limbs.leg')
    
    heel_bone = metarig.data.edit_bones.active
    bone_select_set(heel_bone, False)
    
    # Delete the rest of the leg bones, other than heel
    bpy.ops.armature.delete(confirm=False)
    
    foot_bone = metarig.data.edit_bones.get('foot.L')
    
    if foot_bone:
        heel_bone.parent = foot_bone
        
        bone_select_set(heel_bone, True)
        metarig.data.edit_bones.active = heel_bone
        bpy.ops.armature.symmetrize()


def force_rigify_options_update(obj):
    # When we set a pose bone to a rigify type, the UI will update the UI to show the options.
    # This doesn't happen when we set it using a script however. Selecting anything seems to make
    # the UI to update. So, this is kinda a hacky way to force the rigify options to update.
    obj.select_set(True)


def change_bone_layers(rig, bone_name, layers):
    bpy.ops.pose.select_all(action='DESELECT')
    rig.data.bones.active = rig.data.bones[bone_name]
    bpy.ops.pose.select_linked()
    bpy.ops.pose.bone_layers(layers=layer_params(layers))


def rigify_head(metarig, bone_name, layers):
    pose_bone = metarig.pose.bones[bone_name]
    pose_bone.rigify_type = 'spines.super_head'
    
    force_rigify_options_update(metarig)
    
    params = pose_bone.rigify_parameters
    params.connect_chain = True
    params.tweak_layers_extra = True
    params.tweak_layers = layer_params([4])
    
    change_bone_layers(metarig, bone_name, layers)


def rigify_shoulder(metarig, bone_name, layers):
    pose_bone = metarig.pose.bones[bone_name]
    pose_bone.rigify_type = 'basic.super_copy'
    
    force_rigify_options_update(metarig)
    
    params = pose_bone.rigify_parameters
    params.make_control = True
    params.make_widget = True
    params.super_copy_widget_type = 'shoulder'
    params.make_deform = True
    params.relink_constraints = False
    
    change_bone_layers(metarig, bone_name, layers)


def rigify_arm(metarig, bone_name, layers, fk_layers, tweak_layers):
    pose_bone = metarig.pose.bones[bone_name]
    pose_bone.rigify_type = 'limbs.arm'
    
    force_rigify_options_update(metarig)
    
    params = pose_bone.rigify_parameters
    params.make_ik_wrist_pivot = False
    params.rotation_axis = 'automatic'
    params.segments = 2
    params.bbones = 10
    params.limb_uniform_scale = False
    params.make_custom_pivot = False
    params.ik_local_location = False
    params.fk_layers_extra = True
    params.fk_layers = layer_params(fk_layers)
    params.tweak_layers_extra = True
    params.tweak_layers = layer_params(tweak_layers)
    
    change_bone_layers(metarig, bone_name, layers)


def rigify_spine(metarig, bone_name, layers):
    pose_bone = metarig.pose.bones[bone_name]
    pose_bone.rigify_type = 'spines.basic_spine'
    
    force_rigify_options_update(metarig)
    
    params = pose_bone.rigify_parameters
    params.make_custom_pivot = False
    params.tweak_layers_extra = True
    params.tweak_layers = layer_params([4])
    params.make_fk_controls = True
    params.fk_layers_extra = True
    params.fk_layers = layer_params([4])
    
    change_bone_layers(metarig, bone_name, layers)


def rigify_leg(metarig, bone_name, layers, fk_layers, tweak_layers):
    pose_bone = metarig.pose.bones[bone_name]
    pose_bone.rigify_type = 'limbs.leg'
    
    force_rigify_options_update(metarig)
    
    params = pose_bone.rigify_parameters
    params.foot_pivot_type = 'ANKLE_TOE'
    params.extra_ik_toe = True
    params.rotation_axis = 'automatic'
    params.segments = 2
    params.bbones = 10
    params.limb_uniform_scale = False
    params.make_custom_pivot = False
    params.ik_local_location = False
    params.fk_layers_extra = True
    params.fk_layers = layer_params(fk_layers)
    params.tweak_layers_extra = True
    params.tweak_layers = layer_params(tweak_layers)
    
    change_bone_layers(metarig, bone_name, layers)


def rigify_bust(metarig, bone_name, layers):
    pose_bone = metarig.pose.bones[bone_name]
    pose_bone.rigify_type = 'basic.super_copy'
    
    force_rigify_options_update(metarig)
    
    params = pose_bone.rigify_parameters
    params.make_control = True
    params.make_widget = True
    params.super_copy_widget_type = 'circle'
    params.make_deform = True
    params.relink_constraints = False
    
    change_bone_layers(metarig, bone_name, layers)


def rigify_extra_bones(metarig):
    #TODO
    return


def set_layer_settings(metarig, layer_number, name, row, group):
    layer = metarig.data.rigify_layers[layer_number]
    layer.name = name
    layer.row = row
    layer.group = group


def init_rigify_layers(metarig):
    bpy.ops.armature.rigify_add_bone_groups()
    bpy.ops.pose.rigify_layer_init()
    
    metarig.data.layers = layer_params([0, 3, 5, 7, 10, 13, 16])
    
    # Refer default human meta-rig
    set_layer_settings(metarig, 0, 'Face', 1, 5)
    set_layer_settings(metarig, 1, 'Face (Primary)', 2, 2)
    set_layer_settings(metarig, 2, 'Face (Secondary)', 2, 3)
    
    set_layer_settings(metarig, 3, 'Torso', 3, 3)
    set_layer_settings(metarig, 4, 'Torso (Tweak)', 4, 4)
    
    set_layer_settings(metarig, 5, 'Fingers', 5, 6)
    set_layer_settings(metarig, 6, 'Fingers (Detail)', 6, 5)
    
    set_layer_settings(metarig, 7, 'Arm.L (IK)', 7, 2)
    set_layer_settings(metarig, 8, 'Arm.L (FK)', 8, 5)
    set_layer_settings(metarig, 9, 'Arm.L (Tweak)', 9, 4)
    
    set_layer_settings(metarig, 10, 'Arm.R (IK)', 7, 2)
    set_layer_settings(metarig, 11, 'Arm.R (FK)', 8, 5)
    set_layer_settings(metarig, 12, 'Arm.R (Tweak)', 9, 4)
    
    set_layer_settings(metarig, 13, 'Leg.L (IK)', 10, 2)
    set_layer_settings(metarig, 14, 'Leg.L (FK)', 11, 5)
    set_layer_settings(metarig, 15, 'Leg.L (Tweak)', 12, 4)
    
    set_layer_settings(metarig, 16, 'Leg.R (IK)', 10, 2)
    set_layer_settings(metarig, 17, 'Leg.R (FK)', 11, 5)
    set_layer_settings(metarig, 18, 'Leg.R (Tweak)', 12, 4)
    
    # Root
    metarig.data.rigify_layers[28].group = 1


def setup_rigify(metarig):
    bpy.ops.object.mode_set(mode='POSE')   

    rigify_head(metarig, 'spine.004', layers=[3])
    rigify_shoulder(metarig, 'shoulder.L', layers=[3])
    rigify_shoulder(metarig, 'shoulder.R', layers=[3])
    rigify_arm(metarig, 'upper_arm.L', layers=[7], fk_layers=[8], tweak_layers=[9])
    rigify_arm(metarig, 'upper_arm.R', layers=[10], fk_layers=[11], tweak_layers=[12])
    rigify_spine(metarig, 'spine', layers=[3])
    rigify_leg(metarig, 'thigh.L', layers=[13], fk_layers=[14], tweak_layers=[15])
    rigify_leg(metarig, 'thigh.R', layers=[16], fk_layers=[17], tweak_layers=[18])
    
    for name in find_bust_bone_names(metarig):
        rigify_bust(metarig, name, layers=[3])
    
    rigify_extra_bones(metarig)
    init_rigify_layers(metarig)


def generate_metarig(context):
    vrm_rig = context.view_layer.objects.active
    
    bpy.ops.object.duplicate()
    
    metarig = context.view_layer.objects.active
    metarig.name = vrm_rig.name + '.metarig'
    metarig.data.name = vrm_rig.data.name + '.metarig'
    
    rename_bones(metarig)
    
    remove_unneeded_bones(metarig)
    detach_bone_from_parent(metarig, 'spine.004')
    detach_bone_from_parent(metarig, 'upper_arm.L')
    detach_bone_from_parent(metarig, 'upper_arm.R')
    add_heel_bones(metarig)
    
    setup_rigify(metarig)


class GenerateMetarig(bpy.types.Operator):
    """Generate rigify metarig from vrm armature"""
    bl_idname = "vrm_rigify_helper.generate_metarig"
    bl_label = "Generate Metarig"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_vrm_rig(obj)

    def execute(self, context):
        generate_metarig(context)
        return {'FINISHED'}
