# video_search_engine.py
import os
import json
from download_video import download_video
from scene_detection import detect_scenes, save_scene_images
from captioning import get_scene_caption
from search import fuzzy_search_scenes
from create_collage import create_collage
import moondream as md


def main():
    # Define the directory for scene images
    scenes_dir = "scenes"
    captions_file = "scene_captions.json"

    # Check if scene_captions.json exists and is not empty
    if os.path.exists(captions_file):
        try:
            with open(captions_file, "r") as f:
                scene_captions = json.load(f)
            print("Scene captions loaded.")
        except (json.JSONDecodeError, FileNotFoundError):
            print("Error decoding JSON or file is empty. Regenerating captions...")
            scene_captions = None
    else:
        print("scene_captions.json not found. Regenerating captions...")
        scene_captions = None

    if not scene_captions:
        # Download video based on search query
        search_query = input("Enter the search query: ")
        video_path = download_video(search_query)

        # Detect scenes
        scene_list = detect_scenes(video_path)

        # Save scene images in the specified directory
        scenes_dir = save_scene_images(video_path, scene_list)

        model_path = (
            r"C:\\Users\\Ron\\Downloads\\moondream-0_5b-int8.mf\\moondream-0_5b-int8.mf"
        )
        model = md.vl(model=model_path)

        # Generate captions for each scene
        scene_captions = {}
        for i in range(len(scene_list)):
            image_path = os.path.join(scenes_dir, f"scene_{i}.jpg")
            if os.path.exists(image_path):
                try:
                    caption = get_scene_caption(
                        image_path, model
                    ) 
                    scene_captions[i] = caption
                    print(f"Caption for scene {i}: {caption}")
                except Exception as e:
                    print(f"Error generating caption for scene {i}: {e}")
            else:
                print(f"Image not found: {image_path}")

        # Save captions to JSON file
        with open(captions_file, "w") as f:
            json.dump(scene_captions, f)
        print("Scene captions saved.")

    # Search captions for a specific word
    search_word = input("Enter a word to search for: ")
    matching_scenes = fuzzy_search_scenes(search_word, scene_captions)

    # Create collage from matching scenes
    if matching_scenes:
        create_collage(matching_scenes, scenes_dir)
        print("Collage created and saved as collage.png.")
    else:
        print(f"No matching scenes found for the word: {search_word}")


if __name__ == "__main__":
    main()
