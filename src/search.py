# search.py
from rapidfuzz import fuzz
from prompt_toolkit.completion import Completer, Completion


def fuzzy_search_scenes(search_word, scene_captions, threshold=85):
    matching_scenes = []
    for scene_num, caption in scene_captions.items():
        score = fuzz.partial_ratio(search_word.lower(), caption.lower())
        if score >= threshold:
            matching_scenes.append(scene_num)
    return matching_scenes


# Completer for autocompleting words based on scene captions
class SceneCaptionCompleter(Completer):
    def __init__(self, captions):
        self.captions = captions
        self.words = set()

        # Extract all words from the captions and store them in the set
        for caption in captions.values():
            self.words.update(caption.split())

    def get_completions(self, document, complete_event):
        # Get the word typed so far
        word_so_far = document.text
        # Find words that start with the typed word
        matches = [
            word for word in self.words if word.lower().startswith(word_so_far.lower())
        ]

        # Yield the matches as completions
        for match in matches:
            yield Completion(match, start_position=-len(word_so_far))