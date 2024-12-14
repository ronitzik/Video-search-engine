# search.py
from rapidfuzz import fuzz
from prompt_toolkit.completion import Completer, Completion
import string


def remove_punctuation(text):
    """Remove punctuation from the given text."""
    return text.translate(str.maketrans("", "", string.punctuation))


def fuzzy_search_scenes(search_word, scene_captions, threshold=85):
    matching_scenes = []
    search_word_clean = remove_punctuation(search_word).lower()  # Clean the search word
    for scene_num, caption in scene_captions.items():
        caption_clean = remove_punctuation(caption).lower()  # Clean the caption
        score = fuzz.partial_ratio(search_word_clean, caption_clean)
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
            cleaned_caption = remove_punctuation(caption).lower()  # Clean the captions
            self.words.update(cleaned_caption.split())

    def get_completions(self, document, complete_event):
        # Get the word typed so far
        word_so_far = document.text
        # Clean the word typed so far
        word_so_far_clean = remove_punctuation(word_so_far).lower()

        # Find words that start with the typed word
        matches = [
            word for word in self.words if word.lower().startswith(word_so_far_clean)
        ]

        # Yield the matches as completions
        for match in matches:
            yield Completion(match, start_position=-len(word_so_far))