def is_vrm_rig(obj):
    if not (obj and obj.data and obj.type == 'ARMATURE'):
        return False
    if not obj.data.vrm_addon_extension:
        return False
    meta = obj.data.vrm_addon_extension.vrm0.meta
    if not (meta.title and meta.author):
        return False
    if obj.data.get('extracted_vrm_rig'):
        return False
    return True
    
    
def is_rigify_rig(obj):
    if not (obj and obj.data and obj.type == 'ARMATURE'):
        return False
    if 'rig_id' in obj.data:
        return True
    return False
    
    
def is_metarig(obj):
    if not (obj and obj.data and obj.type == 'ARMATURE'):
        return False
    if 'rig_id' in obj.data:
        return False
    for b in obj.pose.bones:
        if b.rigify_type != "":
            return True
    return False


def is_face_mesh(obj):
    return obj.name and 'face' in obj.name.casefold() and obj.type == 'MESH'


def is_body_mesh(obj):
    return obj.name and 'body' in obj.name.casefold() and obj.type == 'MESH'
