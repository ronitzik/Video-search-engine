# search.py
from rapidfuzz import fuzz


def fuzzy_search_scenes(search_word, scene_captions, threshold=80):
    matching_scenes = []
    for scene_num, caption in scene_captions.items():
        score = fuzz.partial_ratio(search_word.lower(), caption.lower())
        if score >= threshold:
            matching_scenes.append(scene_num)
    return matching_scenes
