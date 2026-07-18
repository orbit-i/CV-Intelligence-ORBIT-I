import json
import os


def load_domains():
    """
    Load domain keywords from domains.json
    """

    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, "..", "data", "domains.json")

    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


def keyword_match(tokens):
    """
    Compare resume tokens against every domain.

    Returns:
    {
        domain:{
            matched:int,
            total_keywords:int,
            matched_keywords:[]
        }
    }
    """

    domains = load_domains()

    cleaned_text = " ".join(tokens)

    results = {}

    for domain, keywords in domains.items():

        matched_keywords = []

        for keyword in keywords:

            keyword = keyword.lower()

            # Multi-word keyword
            if " " in keyword:
                if keyword in cleaned_text:
                    matched_keywords.append(keyword)

            # Single-word keyword
            else:
                if keyword in tokens:
                    matched_keywords.append(keyword)

        results[domain] = {
            "matched": len(matched_keywords),
            "total_keywords": len(keywords),
            "matched_keywords": matched_keywords
        }

    return results