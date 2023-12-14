import bpy


def get_current_visible_layers(context):
    rig = context.view_layer.objects.active
    layer_count = len(rig.data.layers)
    
    current_visible_layers = [False] * layer_count
    
    for idx in range(layer_count):
        current_visible_layers[idx] = rig.data.layers[idx]
        
    return current_visible_layers
