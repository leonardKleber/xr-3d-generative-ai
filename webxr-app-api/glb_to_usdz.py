import bpy
import sys
import os

def reset_blend():
    """Clears the scene ensuring no default cubes/cameras remain."""
    bpy.ops.wm.read_factory_settings(use_empty=True)

def convert_glb_to_usdz(input_file, output_file):
    # 1. Resolve Absolute Paths (Fixes Windows relative path issues)
    abs_input = os.path.abspath(input_file)
    abs_output = os.path.abspath(output_file)

    # 2. Check Input
    if not os.path.exists(abs_input):
        print(f"CRITICAL ERROR: Input file not found at: {abs_input}")
        return

    # 3. Create Output Directory if it doesn't exist (Fixes your specific error)
    output_dir = os.path.dirname(abs_output)
    if output_dir and not os.path.exists(output_dir):
        print(f"Creating missing directory: {output_dir}")
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Error creating directory: {e}")
            return

    # 4. Reset Blender
    reset_blend()

    print(f"--- Importing: {abs_input} ---")
    try:
        bpy.ops.import_scene.gltf(filepath=abs_input)
    except Exception as e:
        print(f"Import Failed: {e}")
        return

    print(f"--- Exporting to: {abs_output} ---")
    try:
        bpy.ops.wm.usd_export(
            filepath=abs_output,
            check_existing=False,
            export_textures=True, 
            selected_objects_only=False,
            root_prim_path='/root',
            export_materials=True,
            generate_preview_surface=True  # Essential for Vision Pro
        )
        print(f"--- SUCCESS: Saved to {abs_output} ---")
    except Exception as e:
        print(f"Export Failed: {e}")

if __name__ == "__main__":
    try:
        # Check arguments after "--"
        if "--" in sys.argv:
            args = sys.argv[sys.argv.index("--") + 1:]
            if len(args) < 2:
                print("Usage: blender ... -- <input.glb> <output.usdz>")
            else:
                convert_glb_to_usdz(args[0], args[1])
        else:
            print("Error: Arguments must be separated by '--'")
    except Exception as e:
        print(f"An error occurred: {e}")