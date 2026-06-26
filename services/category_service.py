CATEGORY_KEYWORDS = {

    "DBMS": [
        "sql",
        "database",
        "normalization",
        "primary key",
        "foreign key",
        "er diagram"
    ],

    "Operating Systems": [
        "process",
        "thread",
        "deadlock",
        "semaphore",
        "cpu scheduling"
    ],

    "Computer Networks": [
        "tcp",
        "udp",
        "router",
        "ip address",
        "network"
    ],

    "Machine Learning": [
        "classification",
        "regression",
        "neural network",
        "training",
        "dataset"
    ],

    "Data Structures": [
        "array",
        "linked list",
        "stack",
        "queue",
        "tree"
    ]
}
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
