# create_collage.py
from PIL import Image
import os


def create_collage(matching_scenes, scenes_dir):
    images = [
        Image.open(os.path.join(scenes_dir, f"scene_{i}.jpg")) for i in matching_scenes
    ]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    collage = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for img in images:
        collage.paste(img, (x_offset, 0))
        x_offset += img.width

    collage.save("collage.png")
    os.system("collage.png")
