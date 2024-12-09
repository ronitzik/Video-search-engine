# scene_detection.py
import cv2
import os
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector


def detect_scenes(video_path, threshold, min_scene_len):
    """
    Detect scenes in the video.
    """
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold, min_scene_len=min_scene_len)
    )
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    print(f"Detected scenes: {len(scene_list)}")

    # Create the scenes folder if it doesn't exist
    if not os.path.exists("scenes"):
        os.makedirs("scenes")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Couldn't open the video file.")
        return []

    scene_images = []

    for i, scene in enumerate(scene_list):
        # Extract the start frame of each scene
        scene_start_frame = scene[0]

        scene_start_frame = int(scene_start_frame)

        # Seek to the start frame of the scene
        cap.set(cv2.CAP_PROP_POS_FRAMES, scene_start_frame)

        # Read the frame at that position
        ret, frame = cap.read()

        # If a frame is successfully read, save the image
        if ret:
            # Save the image to the 'scenes' folder with the scene number as part of the filename
            image_path = f"scenes/scene_{i}.jpg"
            cv2.imwrite(image_path, frame)
            scene_images.append((i, image_path))
        else:
            print(f"Failed to read frame for Scene {i + 1}")

    cap.release()

    video_manager.release()

    return scene_images
