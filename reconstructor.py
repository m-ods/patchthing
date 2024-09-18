def reconstruct_sentences(words: List[Word], sentence_breaks: List[int]): # -> List[dict]:
    # Reconstruct sentence objects from words

    # technically there's no need for sentence breaks because punctuation is attached to the word.
    pass

def reconstruct_paragraphs(sentences: List[Sentence]): # -> List[dict]:
    # Reconstruct paragraph objects from sentences
    pass

# def reconstruct_transcript(original_transcript: dict, new_text: str) -> dict:

#     # basically compare the transcripts then make the changes to old transcript and save it in the db

#     # Tokenize the new text
#     new_words, new_sentences = tokenize_text(new_text)
    
#     # Perform diff between original and new text
#     diffs = list(difflib.ndiff(original_transcript['text'].split(), new_text.split()))
    
#     # Map new words to original words, preserving metadata where possible
#     updated_words = map_words(original_transcript['words'], new_words, diffs)
    
#     # Reconstruct sentences and paragraphs
#     updated_sentences = reconstruct_sentences(updated_words, new_sentences)
#     updated_paragraphs = reconstruct_paragraphs(updated_sentences)
    
#     # Update the transcript object
#     updated_transcript = original_transcript.copy()
#     updated_transcript['text'] = new_text
#     updated_transcript['words'] = updated_words
#     updated_transcript['sentences'] = updated_sentences
#     updated_transcript['paragraphs'] = updated_paragraphs
    
#     return updated_transcript