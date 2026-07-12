import nltk

from nltk.tokenize import sent_tokenize




def generate_summary(content):

    if not content:
        return ""

    sentences = sent_tokenize(
        content
    )


    if len(sentences) <= 3:

        return content


    summary = sentences[:3]


    return " ".join(summary)