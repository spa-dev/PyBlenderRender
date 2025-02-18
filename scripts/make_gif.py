import os
from PIL import Image
import argparse

def create_gif_from_images(image_folder, output_gif, duration=100, loop=0):
    """Creates a GIF from a folder of PNG images.

    Args:
        image_folder (str): Path to the folder containing PNG images.
        output_gif (str): Path to save the output GIF.
        duration (int): Duration for each frame in milliseconds (default: 100ms).
        loop (int): Number of times the GIF should loop (0 for infinite).
    """
    images = []
    
    # Get all PNG files sorted by name
    files = sorted(f for f in os.listdir(image_folder) if f.endswith(".png"))
    
    if not files:
        print("No PNG files found in the folder.")
        return

    for file in files:
        img_path = os.path.join(image_folder, file)
        images.append(Image.open(img_path))

    # Save as GIF
    images[0].save(output_gif, save_all=True, append_images=images[1:], duration=duration, loop=loop)
    print(f"GIF saved at {output_gif}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a folder of PNG images into a GIF.")
    parser.add_argument("image_folder", help="Path to the folder containing PNG images.")
    parser.add_argument("output_gif", help="Path to save the output GIF.")
    parser.add_argument("--duration", type=int, default=100, help="Duration per frame in milliseconds (default: 100ms).")
    parser.add_argument("--loop", type=int, default=0, help="Number of times the GIF should loop (0 for infinite).")

    args = parser.parse_args()
    create_gif_from_images(args.image_folder, args.output_gif, args.duration, args.loop)
    
#Example execution from command line
#python make_gif.py /path/to/images output.gif --duration 200 --loop 0


