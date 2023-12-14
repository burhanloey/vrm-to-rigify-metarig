import bpy


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
