import nltk

from nltk.tokenize import sent_tokenize

nltk.download(
    "punkt",
    quiet=True
)


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