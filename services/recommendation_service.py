from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar_notes(current_note, all_notes):
    if not current_note["content"]:
        return []

    documents = [current_note["content"]]

    note_lookup = []

    for note in all_notes:

        if (
            note["id"] != current_note["id"]
            and note["content"]
        ):

            documents.append(
                note["content"]
            )

            note_lookup.append(note)

    if not note_lookup:
        return []

    vectorizer = TfidfVectorizer()

    tfidf = vectorizer.fit_transform(
        documents
    )

    similarities = cosine_similarity(
        tfidf[0:1],
        tfidf[1:]
    )[0]

    scored_notes = list(
        zip(
            note_lookup,
            similarities
        )
    )

    scored_notes.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return [
        note
        for note, score in scored_notes[:3]
        if score > 0
    ]