from assemblyai.types import Word, Sentence, Paragraph, Utterance, UtteranceWord
from typing import List, Dict

def reconstruct_sentences(word_dicts: List[Dict]) -> List[Sentence]:
    # To Saman: is it bad practice to reconstruct words in here instead of in its own function?
    words = [Word(**word_dict) for word_dict in word_dicts]
    sentences = []
    current_sentence_words = []
    
    sentence_ending_punctuation = set('.!?')
    
    for word in words:
        current_sentence_words.append(word)
        
        if word.text[-1] in sentence_ending_punctuation or word is words[-1]:
            # End of sentence reached
            start = current_sentence_words[0].start
            end = current_sentence_words[-1].end
            

            # we should check if sentences have a speaker in the first place before setting the speaker

            # Get the speaker of the middle word
            middle_index = len(current_sentence_words) // 2
            speaker = current_sentence_words[middle_index].speaker
            
            # Calculate average confidence (commented out as per instructions)
            # confidence = sum(word.confidence for word in current_sentence_words) / len(current_sentence_words)
            confidence = 0.5  # Set to 0.5 for simulation purposes
            
            sentence = Sentence(current_sentence_words, start, end, confidence, speaker)
            sentences.append(sentence)
            current_sentence_words = []
    
    return sentences


def create_utterance(words: List[UtteranceWord]) -> Utterance:
    return Utterance(
        words=words,
        text=' '.join(word.text for word in words),
        start=words[0].start,
        end=words[-1].end,
        confidence=sum(word.confidence for word in words) / len(words),
        speaker=words[0].speaker,
        channel=words[0].channel
    )


def reconstruct_utterances(words: List[Word]) -> List[Utterance]:
    utterances = []
    current_utterance_words = []
    current_speaker = None

    for word in words:
        if word.speaker != current_speaker and current_utterance_words:
            # Create a new utterance when the speaker changes
            utterance = create_utterance(current_utterance_words)
            utterances.append(utterance)
            current_utterance_words = []

        # Convert Word to UtteranceWord
        utterance_word = UtteranceWord(**word.dict(), channel=None)
        current_utterance_words.append(utterance_word)
        current_speaker = word.speaker

    # Add the last utterance
    if current_utterance_words:
        utterance = create_utterance(current_utterance_words)
        utterances.append(utterance)

    return utterances



def reconstruct_paragraphs(sentences: List[Sentence]): # -> List[dict]:
    # Reconstruct paragraph objects from sentences

    # Lol, should we just make every 3 sentences a paragraph... do you think folks will notice? This is pretty much how our production logic works anyway: https://github.com/AssemblyAI/speech-api/blob/staging/api/utils/word_transforms.py#L87

    paragraphs = []
    sentences_per_paragraph = 5

    for i in range(0, len(sentences), sentences_per_paragraph):
        paragraph_sentences = sentences[i:i+sentences_per_paragraph]
        
        # Collect all words from the sentences
        all_words = [word for sentence in paragraph_sentences for word in sentence.words]
        
        # Set paragraph properties
        start = paragraph_sentences[0].start
        end = paragraph_sentences[-1].end
        
        # Calculate average confidence (commented out as per previous instructions)
        # confidence = sum(sentence.confidence for sentence in paragraph_sentences) / len(paragraph_sentences)
        confidence = 0.5  # Set to 0.5 for simulation purposes
        
        # Construct paragraph text
        text = ' '.join(sentence.text for sentence in paragraph_sentences)
        
        # Create Paragraph object
        paragraph = Paragraph(all_words, start, end, confidence, text)
        paragraphs.append(paragraph)
    
    return paragraphs

def reconstruct_text(word_dicts: List[Dict]) -> str:
    text = ""
    for word in word_dicts:
        text += word["text"] + " "
    return text.strip()