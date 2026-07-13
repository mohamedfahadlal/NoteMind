import nltk

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from collections import Counter

import string



def generate_summary(content):

    if not content:
        return ""

    sentences = sent_tokenize(content)

    if len(sentences) <= 3:
        return content

    stop_words = set(stopwords.words("english"))

    words = word_tokenize(content.lower())

    filtered_words = []

    for word in words:

        if (
            word not in stop_words
            and word not in string.punctuation
            and word.isalpha()
        ):
            filtered_words.append(word)

    word_frequencies = Counter(filtered_words)

    sentence_scores = {}

    for sentence in sentences:

        sentence_words = word_tokenize(
            sentence.lower()
        )

        score = 0

        for word in sentence_words:

            score += word_frequencies.get(
                word,
                0
            )

        sentence_scores[sentence] = score

    ranked_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )

    summary = ranked_sentences[:3]

    return " ".join(summary)