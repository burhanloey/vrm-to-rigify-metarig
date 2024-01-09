import bpy

from .checks import is_vrm_rig, is_metarig, is_face_mesh
from .utils.eye_fix import find_face_mesh_object


def deselect_all_objects():
    bpy.ops.object.select_all(action='DESELECT')
    
    
def deselect_all_pose_bones():
    bpy.ops.pose.select_all(action='DESELECT')
    
    
def set_active(context, obj):
    obj.select_set(True)
    context.view_layer.objects.active = obj


def do_bone_alignments():
    bpy.ops.vrm_rigify_helper.align_head_bone()  # yes, singular bone
    bpy.ops.vrm_rigify_helper.align_hand_bones()
    bpy.ops.vrm_rigify_helper.align_feet_bones()


def copy_rigify_settings(source, destination):
    destination.data.rigify_target_rig = source.data.rigify_target_rig
    destination.data.rigify_rig_ui = source.data.rigify_rig_ui
    destination.data.rigify_widgets_collection = source.data.rigify_widgets_collection


def transfer_meshes(context, source, destination):
    deselect_all_objects()
    set_active(context, source)
    bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
    
    for obj in context.selected_objects:
        if obj.type != 'MESH':
            obj.select_set(False)
    
    set_active(context, destination)
    bpy.ops.object.parent_set(type='OBJECT')


def update_meshes_armature_modifiers(context, rig):
    deselect_all_objects()
    set_active(context, rig)
    bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
    
    for mesh in context.selected_objects:
        mesh.modifiers['Armature'].object = rig


def post_generate_setup(context, rigify_rig):
    deselect_all_objects()
    set_active(context, rigify_rig)
    
    bpy.ops.vrm_rigify_helper.remove_unused_bones()
    
    bpy.ops.object.select_hierarchy(direction='CHILD', extend=False)
    
    face_mesh = find_face_mesh_object(context.selected_objects)
    
    deselect_all_objects()
    set_active(context, rigify_rig)
    face_mesh.select_set(True)
    
    bpy.ops.vrm_rigify_helper.fix_eye_direction()
    bpy.ops.vrm_rigify_helper.enable_cloth_follow()
    bpy.ops.vrm_rigify_helper.disable_all_ik_stretch()
    
    deselect_all_pose_bones()
    
    bpy.ops.vrm_rigify_helper.show_default_visible_layers()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    deselect_all_objects()
    set_active(context, rigify_rig)


def generate(context):
    vrm_rig = context.view_layer.objects.active

    bpy.ops.vrm_rigify_helper.generate_metarig()
    
    metarig = context.view_layer.objects.active
    
    do_bone_alignments()
    
    # Set Rig Name if it is not specified in Rigify settings
    if not metarig.data.rigify_rig_basename:
        metarig.data.rigify_rig_basename = metarig.name.replace('metarig', 'rig')
    
    bpy.ops.object.duplicate()
    
    duplicate_metarig = context.view_layer.objects.active
    
    bpy.ops.pose.rigify_upgrade_face()
    bpy.ops.pose.rigify_generate()
    
    copy_rigify_settings(source=duplicate_metarig, destination=metarig)
    
    rigify_rig = context.view_layer.objects.active
    rigify_rig.show_in_front = True
    
    transfer_meshes(context, source=vrm_rig, destination=rigify_rig)
    update_meshes_armature_modifiers(context, rigify_rig)
    
    # Cleanup duplicate metarig
    deselect_all_objects()
    set_active(context, duplicate_metarig)
    
    bpy.ops.object.delete(use_global=True, confirm=False)
    
    post_generate_setup(context, rigify_rig)
    
    
def regenerate(context):
    metarig = context.view_layer.objects.active
    
    bpy.ops.object.duplicate()
    
    duplicate_metarig = context.view_layer.objects.active
    
    bpy.ops.pose.rigify_upgrade_face()
    bpy.ops.pose.rigify_generate()
    
    rigify_rig = context.view_layer.objects.active
    rigify_rig.show_in_front = True
    
    # Cleanup duplicate metarig
    deselect_all_objects()
    set_active(context, duplicate_metarig)
    
    bpy.ops.object.delete(use_global=True, confirm=False)
    
    post_generate_setup(context, rigify_rig)
    

def has_children_that_is_not_collider(obj):
    for child in obj.children:
        if 'collider' not in child.name.casefold():
            return True
    return False


class OneClickSetup(bpy.types.Operator):
    """Setup everything using the operators"""
    bl_idname = "vrm_rigify_helper.one_click_setup"
    bl_label = "One-Click Setup"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_vrm_rig(obj) and has_children_that_is_not_collider(obj)

    def execute(self, context):
        generate(context)
        return {'FINISHED'}


class Regenerate(bpy.types.Operator):
    """Regenerate using the metarig"""
    bl_idname = "vrm_rigify_helper.regenerate"
    bl_label = "Regenerate"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.view_layer.objects.active
        return is_metarig(obj)

    def execute(self, context):
        regenerate(context)
        return {'FINISHED'}
