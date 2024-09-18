# i use ice-cream to make the JSON output readable
from icecream import ic

import reconstructor
from utils import dictify, update_assemblyai_words

old_text = "Here's what's going to happen. I am going to have to fix you, manage you to on a more personal scale, a more micro form of management. Jim. What is that called? Microjiment."

old_words = [
    {
        "text": "Here's",
        "start": 1840,
        "end": 1968,
        "confidence": 0.88174,
        "speaker": None,
    },
    {
        "text": "what's",
        "start": 1968,
        "end": 2096,
        "confidence": 0.53775,
        "speaker": None,
    },
    {
        "text": "going",
        "start": 2096,
        "end": 2208,
        "confidence": 0.99138,
        "speaker": None,
    },
    {"text": "to", "start": 2214, "end": 2366, "confidence": 1, "speaker": None},
    {
        "text": "happen.",
        "start": 2398,
        "end": 2662,
        "confidence": 0.95412,
        "speaker": None,
    },
    {"text": "I", "start": 2726, "end": 2854, "confidence": 1, "speaker": None},
    {"text": "am", "start": 2862, "end": 3006, "confidence": 0.88, "speaker": None},
    {
        "text": "going",
        "start": 3038,
        "end": 3158,
        "confidence": 0.9992,
        "speaker": None,
    },
    {"text": "to", "start": 3174, "end": 3326, "confidence": 1, "speaker": None},
    {
        "text": "have",
        "start": 3358,
        "end": 3502,
        "confidence": 0.99551,
        "speaker": None,
    },
    {"text": "to", "start": 3526, "end": 3950, "confidence": 1, "speaker": None},
    {"text": "fix", "start": 4070, "end": 4438, "confidence": 0.99728, "speaker": None},
    {
        "text": "you,",
        "start": 4494,
        "end": 4854,
        "confidence": 0.99531,
        "speaker": None,
    },
    {
        "text": "manage",
        "start": 4942,
        "end": 5334,
        "confidence": 0.99925,
        "speaker": None,
    },
    {"text": "you", "start": 5422, "end": 5814, "confidence": 0.99683, "speaker": None},
    {"text": "to", "start": 5902, "end": 6390, "confidence": 0.67, "speaker": None},
    {"text": "on", "start": 6510, "end": 6742, "confidence": 0.99611, "speaker": None},
    {"text": "a", "start": 6766, "end": 6902, "confidence": 1, "speaker": None},
    {
        "text": "more",
        "start": 6926,
        "end": 7182,
        "confidence": 0.99887,
        "speaker": None,
    },
    {
        "text": "personal",
        "start": 7246,
        "end": 7850,
        "confidence": 0.99995,
        "speaker": None,
    },
    {
        "text": "scale,",
        "start": 8270,
        "end": 9050,
        "confidence": 0.56566,
        "speaker": None,
    },
    {"text": "a", "start": 9350, "end": 9926, "confidence": 0.55, "speaker": None},
    {
        "text": "more",
        "start": 10038,
        "end": 10334,
        "confidence": 0.99605,
        "speaker": None,
    },
    {
        "text": "micro",
        "start": 10382,
        "end": 10902,
        "confidence": 0.76,
        "speaker": None,
    },
    {
        "text": "form",
        "start": 11006,
        "end": 11246,
        "confidence": 0.98334,
        "speaker": None,
    },
    {"text": "of", "start": 11278, "end": 11470, "confidence": 1, "speaker": None},
    {
        "text": "management.",
        "start": 11510,
        "end": 11902,
        "confidence": 0.99921,
        "speaker": None,
    },
    {
        "text": "Jim.",
        "start": 12006,
        "end": 12286,
        "confidence": 0.95769,
        "speaker": None,
    },
    {
        "text": "What",
        "start": 12318,
        "end": 12438,
        "confidence": 0.99862,
        "speaker": None,
    },
    {
        "text": "is",
        "start": 12454,
        "end": 12534,
        "confidence": 0.99209,
        "speaker": None,
    },
    {
        "text": "that",
        "start": 12542,
        "end": 12662,
        "confidence": 0.99319,
        "speaker": None,
    },
    {
        "text": "called?",
        "start": 12686,
        "end": 13014,
        "confidence": 0.99652,
        "speaker": None,
    },
    {
        "text": "Microjiment.",
        "start": 13102,
        "end": 13926,
        "confidence": 0.08908,
        "speaker": None,
    },
]

new_text = "Here's what's going to happen. I am going to have to fix you, manage you two on a more personal level, a more micro form of management. Jim, What is that called again? Micro-gement."

updated_words = update_assemblyai_words(old_words, old_text, new_text)
words = reconstructor.reconstruct_words(updated_words)
ic(updated_words)

print(reconstructor.reconstruct_text(words, from_word=True))
print("---------------")
print(dictify(reconstructor.reconstruct_sentences(words)))
print("---------------")
print(dictify(reconstructor.reconstruct_utterances(words)))
print("---------------")
print(
    dictify(
        reconstructor.reconstruct_paragraphs(reconstructor.reconstruct_sentences(words))
    )
)
print("---------------")
