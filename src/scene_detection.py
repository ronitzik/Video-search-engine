# scene_detection.py
import cv2
import os
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from skimage.metrics import structural_similarity as ssim


def detect_scenes(
    video_path, threshold=30.0, similarity_threshold=0.9, min_scene_duration=15
):
    """
    Detect scenes in the video and filter out similar scenes.
    - threshold: Sensitivity of the scene detection.
    - similarity_threshold: Minimum similarity score below which two scenes are considered different.
    - min_scene_duration: Minimum duration of a scene in frames.
    """
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()

    # Filter out similar scenes and short scenes
    filtered_scene_list = []
    prev_scene_end_frame = -1
    for i, (start_frame, end_frame) in enumerate(scene_list):
        scene_duration = end_frame - start_frame

        if scene_duration < min_scene_duration:  # Skip very short scenes
            continue

        # Always add the first scene
        if prev_scene_end_frame == -1:
            filtered_scene_list.append((start_frame, end_frame))
            prev_scene_end_frame = end_frame
        else:
            # Extract frames of consecutive scenes to compare them
            prev_scene_image = extract_frame(video_path, prev_scene_end_frame)
            current_scene_image = extract_frame(video_path, start_frame)

            similarity = calculate_image_similarity(
                prev_scene_image, current_scene_image
            )

            if (
                similarity < similarity_threshold
            ):  # Only add if the scenes are sufficiently different
                filtered_scene_list.append((start_frame, end_frame))
                prev_scene_end_frame = end_frame

    return filtered_scene_list


def extract_frame(video_path, frame_number):
    """Extract a frame from the video at a specific frame number."""
    video_capture = cv2.VideoCapture(video_path)

    frame_number = int(frame_number)

    # Check that the frame number is valid
    if frame_number < 0:
        raise ValueError(f"Invalid frame number: {frame_number}")

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video_capture.read()

    if not ret:
        raise RuntimeError(f"Error extracting frame {frame_number} from video")

    return frame


def calculate_image_similarity(image1, image2):
    """Calculate structural similarity between two images."""
    # Convert to grayscale to simplify comparison
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute Structural Similarity Index (SSI)
    similarity, _ = ssim(gray1, gray2, full=True)
    return similarity


# Function to save scene images in a new directory
def save_scene_images(video_path, scene_list):
    """
    Save the images of distinct scenes to a 'scenes' directory.
    """
    # Create a directory named 'scenes' if it doesn't exist
    scenes_dir = "scenes"
    if not os.path.exists(scenes_dir):
        os.makedirs(scenes_dir)

    video_capture = cv2.VideoCapture(video_path)
    for i, scene in enumerate(scene_list):
        start_frame = scene[0]  # Use the start frame of the scene
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, float(start_frame))
        ret, frame = video_capture.read()
        if ret:
            # Save the scene image in the 'scenes' directory
            scene_image_path = os.path.join(scenes_dir, f"scene_{i}.jpg")
            cv2.imwrite(scene_image_path, frame)
    video_capture.release()
    return scenes_dir  # Return the directory path where images are saved
