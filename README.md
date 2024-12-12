# Video Search Engine

This project implements a video search engine that can search for scenes in videos based on their content. The system uses `gemini-1.5-flash` LLM model, `moondream2` and `scenedetect` python libraries (and more) to download videos, detect scenes, generate captions, and perform advanced text-based search.

## Features
- Download videos from YouTube using `yt-dlp`.
- Detect scenes in the downloaded video using `pyscenedetect`.
- Use `moondream2` to generate captions for each scene.
- Store scene captions in a `scene_captions.json` file as a dictionary.
- Search video scenes using user-defined keywords.
- Search using both an **image model** and a **video model**.
  - The **image model** searches based on the captions of the scenes.
  - The **video model** uses a multi-modal model from Google Gemini for video understanding.
- Display and save a collage of all matching scenes based on the search query.
- Use `prompt_toolkit` for autocomplete suggestions while typing in the search query.

## Technologies Used
- **yt-dlp**: A video downloader for YouTube and other sites.
- **pyscenedetect**: A Python library for video scene detection.
- **moondream2**: An image-to-text model for generating captions.
- **Gemini Video Understanding**: Google's multi-modal AI model for video analysis.
- **rapidfuzz**: A library for fuzzy string matching (used for finding similar words in captions).
- **prompt_toolkit**: A Python library for building interactive command-line applications with autocompletion.

## How It Works

### 1. Download Video
The program starts by downloading a YouTube video based on a search query using `yt-dlp`. For example, you can search for the "Super Mario movie trailer."

### 2. Scene Detection
After downloading the video, `pyscenedetect` is used to detect scenes in the video. The number of scenes and their content is adjusted by tweaking the parameters of `pyscenedetect`. Around 50-80 scenes are detected, and their images are saved in the `scenes` directory.

### 3. Captioning
Each scene's image is passed through the `moondream2` model to generate a caption describing the content of the scene. These captions are stored in a JSON file called `scene_captions.json`.

### 4. Search Functionality
- **Image Model Search**: The program allows the user to search scenes based on captions. The user can input a word, and the program will return the scenes that contain that word.
- **Video Model Search**: The user can opt to use a video model (Google Gemini) to search the video for a specific query. The model processes the video to understand the content, and the program extracts frames matching the query.

### 5. Collage Creation
Once the matching scenes are found, a collage of the scene images is created and displayed to the user. The collage is saved as `collage.png`.
