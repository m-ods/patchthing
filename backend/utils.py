import difflib
from typing import Dict, List


def dictify(pydantic_models_list) -> List[Dict]:
    return [i.dict() for i in pydantic_models_list]


def split_into_words(text):
    return text.split()


def update_assemblyai_words(assemblyai_words, old_text, new_text):
    old_words = split_into_words(old_text)
    new_words = split_into_words(new_text)

    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    opcodes = matcher.get_opcodes()

    result = []
    word_index = 0

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            result.extend(assemblyai_words[i1:i2])
            word_index = i2

        elif tag == "replace":
            for i in range(j1, j2):
                if i - j1 < i2 - i1:  # We have an AssemblyAI word to base this on
                    new_word = assemblyai_words[word_index + (i - j1)].copy()
                    new_word["text"] = new_words[i]
                    new_word["confidence"] = 0.5  # Lower confidence for changed words
                else:  # This is an additional word
                    prev_word = (
                        result[-1] if result else assemblyai_words[word_index - 1]
                    )
                    new_word = {
                        "text": new_words[i],
                        "start": prev_word["end"],
                        "end": prev_word["end"]
                        + (prev_word["end"] - prev_word["start"]),
                        "confidence": 0.5,
                        "speaker": prev_word["speaker"],
                    }
                result.append(new_word)
            word_index = i2

        elif tag == "insert":
            for i in range(j1, j2):
                prev_word = result[-1] if result else assemblyai_words[word_index - 1]
                new_word = {
                    "text": new_words[i],
                    "start": prev_word["end"],
                    "end": prev_word["end"] + (prev_word["end"] - prev_word["start"]),
                    "confidence": 0.5,
                    "speaker": prev_word["speaker"],
                }
                result.append(new_word)

        elif tag == "delete":
            word_index = i2

    return result
