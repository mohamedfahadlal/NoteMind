import re


def split_into_paragraphs(content):

    if not content:
        return []

    paragraphs = re.split(r"\n\s*\n", content)

    paragraphs = [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]

    return paragraphs


def extract_keywords(question):

    question = question.lower()

    words = re.findall(r"\b[a-zA-Z]+\b", question)

    stop_words = {
        "what",
        "is",
        "are",
        "the",
        "a",
        "an",
        "of",
        "to",
        "how",
        "why",
        "when",
        "where",
        "does",
        "do",
        "can",
        "explain",
        "define",
        "tell",
        "about"
    }

    keywords = []

    for word in words:

        if word not in stop_words:

            keywords.append(word)

    return keywords



def find_best_paragraph(
    content,
    question
):

    paragraphs = split_into_paragraphs(
        content
    )

    if not paragraphs:
        return None

    keywords = extract_keywords(
        question
    )

    best_paragraph = None

    best_score = 0

    for paragraph in paragraphs:

        score = 0

        paragraph_lower = paragraph.lower()

        for keyword in keywords:

            score += paragraph_lower.count(
                keyword
            )

        if score > best_score:

            best_score = score

            best_paragraph = paragraph

    return best_paragraph