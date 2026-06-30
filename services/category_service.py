from services.keywords import CATEGORY_KEYWORDS

from services.keywords import CATEGORY_KEYWORDS


def categorize_note(content):

    if not content:
        return None

    content = content.lower()

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword.lower() in content:
                score += 1

        scores[category] = score

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:
        return None

    return best_category