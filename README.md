# VRM To Rigify Metarig

Generate Rigify armature and metarig from VRM model

## Requirements

1. [Blender 3.6](https://www.blender.org/download/lts/) or earlier version (does not work on 4.0 and above, yet)
2. [VRM Add-on for Blender](https://vrm-addon-for-blender.info/en/)

## Installation

1. Download `vrm_to_rigify_metarig.zip` from releases page.
2. Install the addon in Blender at `Edit` > `Preferences` > `Add-ons`.
3. Tick the box to enable the addon.

## Usage

### Generate metarig and Rigify rig

1. Import a VRM model using VRM Add-on for Blender (`File` > `Import` > `VRM`).
2. Select the imported armature model.
3. Open 3D viewport sidebar panel (press `N`).
4. Go to `VRM To Rigify Metarig` tab.
5. Click `One-Click Setup`.

### Regenerate Rigify rig

If the metarig and the Rigify rig has already been generated, you can make changes to the metarig (for e.g. enabling finger IK control) and regenerate the Rigify rig.

After the Rigify rig has been generated, the `One-Click Setup` will change to `Regenerate` when you select the metarig.

You can regenerate using Rigify's own control, but by doing so, you will missing out on the post-generate setup like unused bones removal and eye direction fix.

### Eye direction and recalibration

The eye bones generated by VRoid Studio are not aligned to the eye meshes. This will cause the eye to not track the eye control bone.

<p align="center"><img src="docs/vrm_eye_bones_position.png" width="192px"></p>

This addon will try to fix the eye direction by using the middle point of the iris mesh. However, some models have a peculiar shape of iris mesh causing the pupil to not be in the middle. To deal with this issue, this addon provides a utility to recalibrate the eye direction manually.

To recalibrate the eye direction:

1. Position 3D Cursor right at the pupil of the **LEFT** eye (`Shift`+`RMB` for default keymapping, `LMB` for right-click select keymapping).
    - Another way is to go to edit mode and select the vertex (or vertices) that is located at the pupil. Then, snap the cursor (`Mesh` > `Snap` > `Cursor to Selected`).
    - You can also create an empty and adjust the position of the empty to the pupil, then snap the 3D cursor to it (`Object` > `Snap` > `Cursor to Selected`).
2. Click `Recalibrate Eye Direction` under `Utilities` panel.

### Look at object

1. Select both the Rigify rig and the object you want your character to look at. Make sure the Rigify rig is active (yellow text).

<p align="center"><img src="docs/look_at_selection.png" width="304px"></p>
   
2. Click `Look At Object` under `Utilities` panel.

### Other utilities

1. Enable/disable IK stretch for all limbs.
2. Hide/show toon shader. Useful for low performance hardware.
3. Show default/show all control layers.

## Other similar addons

- [vrm-rigify](https://github.com/nanoskript/vrm-rigify)
- [VRigify](https://github.com/Silvergust/VRigify)

## License

MIT License
