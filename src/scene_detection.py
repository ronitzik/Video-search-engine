# scene_detection.py
import os
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import save_images


def detect_scenes(video_path, output_folder):
    """Detect scenes and save images to the output folder."""
    # Check if scenes already exist
    if os.path.exists(output_folder) and any(f.endswith(".jpg") for f in os.listdir(output_folder)):
        print(f"Skipping scene detection because scenes are already exist..")
        return

    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=30.0))
    video_manager.set_downscale_factor()
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    # Retrieve the list of detected scenes
    scenes = scene_manager.get_scene_list()
    print(f"Detected {len(scenes)} scenes.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save images for each scene
    save_images(
        scene_list=scenes,
        video=video_manager,
        num_images=1,
        frame_margin=1,
        image_extension='jpg',
        encoder_param=95,
        image_name_template='$VIDEO_NAME-Scene-$SCENE_NUMBER-$IMAGE_NUMBER',
        output_dir=output_folder,
        show_progress=True,
    )

    video_manager.release()