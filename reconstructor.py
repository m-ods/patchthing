from typing import Dict, List

from assemblyai.types import Paragraph, Sentence, Utterance, UtteranceWord, Word

from utils import dictify


def reconstruct_words(word_dicts: List[Dict]) -> List[Word]:
    return [Word(**word_dict) for word_dict in word_dicts]


def reconstruct_sentences(words: List[Word]) -> List[Sentence]:
    sentences = []
    current_sentence_words = []

    sentence_ending_punctuation = set(".!?")

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
            sentence = Sentence(
                words=current_sentence_words,
                text=reconstruct_text(current_sentence_words, from_word=True),
                start=start,
                end=end,
                confidence=confidence,
                speaker=speaker,
            )
            sentences.append(sentence)
            current_sentence_words = []

    return sentences


def create_utterance(words: List[UtteranceWord]) -> Utterance:
    return Utterance(
        words=words,
        text=reconstruct_text(words, from_word=True),
        start=words[0].start,
        end=words[-1].end,
        confidence=sum(word.confidence for word in words) / len(words),
        speaker=words[0].speaker,
        channel=words[0].channel,
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


def reconstruct_paragraphs(sentences: List[Sentence]) -> List[Paragraph]:
    # Reconstruct paragraph objects from sentences

    # Lol, should we just make every 3 sentences a paragraph... do you think folks will notice? This is pretty much how our production logic works anyway: https://github.com/AssemblyAI/speech-api/blob/staging/api/utils/word_transforms.py#L87

    paragraphs = []
    sentences_per_paragraph = 5

    for i in range(0, len(sentences), sentences_per_paragraph):
        paragraph_sentences = sentences[i : i + sentences_per_paragraph]

        # Collect all words from the sentences
        all_words = [
            word for sentence in paragraph_sentences for word in sentence.words
        ]

        # Set paragraph properties
        start = paragraph_sentences[0].start
        end = paragraph_sentences[-1].end

        # Calculate average confidence (commented out as per previous instructions)
        # confidence = sum(sentence.confidence for sentence in paragraph_sentences) / len(paragraph_sentences)
        confidence = 0.5  # Set to 0.5 for simulation purposes

        # Create Paragraph object
        paragraph = Paragraph(
            words=all_words,
            text=reconstruct_text(all_words, from_word=True),
            start=start,
            end=end,
            confidence=confidence,
        )
        paragraphs.append(paragraph)

    return paragraphs


def reconstruct_transcript(transcript: Dict, words: List[Dict]) -> Dict:
    transcript["words"] = dictify(reconstruct_words(words))
    transcript["utterances"] = dictify(reconstruct_utterances(words))
    sentences = reconstruct_sentences(words)
    transcript["sentences"] = dictify(sentences)
    transcript["paragraphs"] = dictify(reconstruct_paragraphs(sentences))
    return transcript


def reconstruct_text(word_dicts: List[Dict], from_word=False) -> str:
    text = ""
    for word in word_dicts:
        word_text = word.text if from_word else word["text"]
        text += word_text + " "
    return text.strip()
