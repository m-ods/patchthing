import difflib
from dotenv import load_dotenv
import os

def compare_sentences(old_sentence, new_sentence):
    d = difflib.Differ()
    diff = list(d.compare(old_sentence.split(), new_sentence.split()))
    print(diff)
    return ' '.join([token[2:] for token in diff if token.startswith('+ ') or token.startswith('- ')])

old_sentence = "Boom. Yes. Now, Jim is going to be the client, Dwight. You're going to have to sell to him without being aggressive, hostile, or difficult. Let's go."
new_sentence = "Boom. Yes. Now, Jim is going to be the client. Dwight, You're going to have to sell to him without being aggressive, hostile, or difficult. Let's go."





difference = compare_sentences(old_sentence, new_sentence)
print(f"Difference: {difference}")