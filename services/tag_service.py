TAG_KEYWORDS = [
    "sql",
    "normalization",
    "primary key",
    "foreign key",
    "er diagram",
    "deadlock",
    "process",
    "thread",
    "semaphore",
    "tcp",
    "udp",
    "router",
    "ip address",
    "array",
    "linked list",
    "stack",
    "queue",
    "tree",
    "classification",
    "regression",
    "dataset",
    "neural network"
]


def extract_tags(content):

    if not content:
        return []

    content = content.lower()

    found_tags = []

    for tag in TAG_KEYWORDS:

        if tag.lower() in content:
            found_tags.append(tag.title())

    return found_tags
