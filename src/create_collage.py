# create_collage.py
from PIL import Image
import os
import math


def create_collage(matching_scenes, scenes_dir):
    # Open all the images from the matching scenes
    images = [
        Image.open(os.path.join(scenes_dir, f"scene_{i}.jpg")) for i in matching_scenes
    ]

    # Get the width and height of all images
    widths, heights = zip(*(i.size for i in images))

    # Define the number of images per row for a grid layout
    num_images = len(images)
    num_columns = int(math.ceil(math.sqrt(num_images))) 
    num_rows = int(math.ceil(num_images / num_columns))  

    # Calculate the width and height of the final collage
    max_width = max(widths)
    total_width = num_columns * max_width
    total_height = sum(heights[i] for i in range(num_rows))

    # Create a new image to hold the collage
    collage = Image.new("RGB", (total_width, total_height))

    # Place each image in the collage grid
    x_offset = 0
    y_offset = 0
    for i, img in enumerate(images):
        collage.paste(img, (x_offset, y_offset))

        # Update the offsets for the next image
        if (i + 1) % num_columns == 0:
            x_offset = 0
            y_offset += max(heights)
        else:
            x_offset += max_width

    # Save the collage image
    collage.save("collage.png")
    os.system("collage.png") 
