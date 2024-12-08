# captioning.py
from PIL import Image
import os


def get_scene_caption(image_path, model):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        image = Image.open(image_path).convert("RGB")
        encoded_image = model.encode_image(image)
        caption_data = model.caption(encoded_image)
        caption = caption_data.get("caption", "No caption available")
        return caption
    except Exception as e:
        raise RuntimeError(f"Error generating caption for {image_path}: {e}")