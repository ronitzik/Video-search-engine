# main.py
import os
import json
from download_video import download_video
from scene_detection import detect_scenes
from captioning import get_scene_caption
from search import fuzzy_search_scenes, SceneCaptionCompleter
from create_collage import create_collage_for_video, create_collage_for_images
import moondream as md
from prompt_toolkit import prompt
from gemini_video_model import analyze_video, extract_frames


def main():
    # Define the directory for scene images
    scenes_dir = "scenes"
    captions_file = "scene_captions.json"

    # Ask the user for a search query and download the video
    search_query = input("Enter the search query: ")
    video_path = download_video(search_query)

    # Ask the user whether they want to use an image model or video model
    model_type = input(
        "Would you like to search the video using an image model (1) or a video model (2)? "
    )

    if model_type == "1":
        # Existing logic (image model)
        use_image_model(video_path, scenes_dir, captions_file)
    elif model_type == "2":
        # New logic (video model)
        use_video_model(video_path, scenes_dir)
    else:
        print("Invalid choice. Please select 1 for image model or 2 for video model.")


def use_image_model(video_path, scenes_dir, captions_file):
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
        # Detect scenes and return scene list with paths for images
        scene_list = detect_scenes(video_path, threshold=30.0, min_scene_len=15)

        # Initialize the model once
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
                    caption = get_scene_caption(image_path, model)
                    scene_captions[i] = caption
                    print(f"Caption for scene {i}: {caption}")
                except Exception as e:
                    print(f"Error generating caption for scene {i}: {e}")

        # Save captions to JSON file
        with open(captions_file, "w") as f:
            json.dump(scene_captions, f)
        print("Scene captions saved.")

    # Setup the completer with all the words from scene captions
    caption_completer = SceneCaptionCompleter(scene_captions)

    # Search captions for a specific word using autocomplete
    search_word = prompt("Search the video using a word: ", completer=caption_completer)

    matching_scenes = fuzzy_search_scenes(search_word, scene_captions)

    # Create collage from matching scenes
    if matching_scenes:
        create_collage_for_images(matching_scenes, scenes_dir)
        print("Collage created and saved as collage.png.")
    else:
        print(f"No matching scenes found for the word: {search_word}")


def use_video_model(video_path, scenes_dir):
    # Ask the user what they want to find in the video
    search_query = input(
        "Using a video model. What would you like me to find in the video? "
    )

    # Get the scenes that match the user input
    timestamps = analyze_video(video_path, search_query)
    print(timestamps)
    if timestamps:
        # Extract frames at the specified timestamps
        extracted_frames = extract_frames(video_path, timestamps, scenes_dir)

        # Create a collage from the extracted frames
        create_collage_for_video(extracted_frames, scenes_dir)
        print("Collage created and saved as collage.png.")
    else:
        print(f"No scenes found matching the description: {search_query}")


if __name__ == "__main__":
    main()