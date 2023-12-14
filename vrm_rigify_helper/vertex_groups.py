import bpy


BONE_PAIRS_MAPPINGS = {
    'UpperArm': 'upper_arm',
    'LowerArm': 'forearm',
    'Shoulder': 'shoulder',
    'UpperLeg': 'thigh',
    'LowerLeg': 'shin',
    'Bust1': 'breast',
    'Foot': 'foot',
    'ToeBase': 'toe',
    'Hand': 'hand',
    'FaceEye': 'eye',
    
    'Thumb1': 'thumb.01',
    'Thumb2': 'thumb.02',
    'Thumb3': 'thumb.03',
    
    'Index1': 'f_index.01',
    'Index2': 'f_index.02',
    'Index3': 'f_index.03',
    
    'Middle1': 'f_middle.01',
    'Middle2': 'f_middle.02',
    'Middle3': 'f_middle.03',
    
    'Ring1': 'f_ring.01',
    'Ring2': 'f_ring.02',
    'Ring3': 'f_ring.03',
    
    'Little1': 'f_pinky.01',
    'Little2': 'f_pinky.02',
    'Little3': 'f_pinky.03',
}

BONE_SINGLES_MAPPINGS = {
    'Hips': 'spine',
    'Spine': 'spine.001',
    'Chest': 'spine.002',
    'UpperChest': 'spine.003',
    'Neck': 'spine.004',
    'Head': 'spine.006',
}


def rename_vrm_vertex_groups_to_rigify(context):
    objs = context.selected_objects

    for obj in objs:
        for vg in obj.vertex_groups:
            name = vg.name
            
            if len(name) <= 2:
                continue
            
            if name in BONE_SINGLES_MAPPINGS:
                new_name = 'DEF-' + BONE_SINGLES_MAPPINGS[name]
                vg.name = new_name
                continue
            
            part = name[:-2]
            
            if part in BONE_PAIRS_MAPPINGS:
                direction = name[-1:]
                new_name = 'DEF-' + BONE_PAIRS_MAPPINGS[part] + '.' + direction
                vg.name = new_name
                continue
            
            if not name.startswith('DEF-'):
                new_name = 'DEF-' + name
                vg.name = new_name


class RenameVRMVertexGroupsToRigify(bpy.types.Operator):
    """Warning! Destructive operation. Consider making duplicates of the meshes or re-import if you want the original vertex group names"""
    bl_idname = "vrm_rigify_helper.rename_vrm_vertex_groups_to_rigify"
    bl_label = "Rename VRM Vertex Groups to Rigify"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        objs = context.selected_objects
        if not objs:
            return False
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                return False
        return True

    def execute(self, context):
        rename_vrm_vertex_groups_to_rigify(context)
        return {'FINISHED'}
