from services.keywords import CATEGORY_KEYWORDS

def extract_tags(content):

    if not content:
        return []

    content = content.lower()

    found_tags = set()

    for keywords in CATEGORY_KEYWORDS.values():

        for keyword in keywords:

            if keyword.lower() in content:

                found_tags.add(keyword)

    return sorted(found_tags)