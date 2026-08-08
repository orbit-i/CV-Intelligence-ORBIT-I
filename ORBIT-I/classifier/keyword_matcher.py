import os
import sqlite3
import re


def load_domains():
    db_path = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'orbit.db')
    )
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT domain_name, keywords FROM domains")
    rows = cursor.fetchall()
    conn.close()

    domains = {}
    for domain_name, keywords_str in rows:
        if keywords_str:
            keywords = [k.strip().lower() for k in keywords_str.split(",") if k.strip()]
        else:
            keywords = []
        domains[domain_name] = keywords
    return domains


def keyword_match(preprocessed):
    """
    Compare resume tokens/text against every domain's keyword list.

    Accepts the dict returned by preprocess_text():
        { "tokens": [...], "full_text": "..." }

    Returns:
    {
        domain: {
            matched: int,
            total_keywords: int,
            matched_keywords: [str, ...]
        }
    }
    """
    domains = load_domains()

    tokens = preprocessed["tokens"]        # deduplicated word list
    full_text = preprocessed["full_text"]  # full clean string (no dedup)
    token_set = set(tokens)

    results = {}

    for domain, keywords in domains.items():
        matched_keywords = []
        seen_matches = set()  # avoid double-counting

        for keyword in keywords:
            keyword = keyword.lower().strip()
            if not keyword or keyword in seen_matches:
                continue

            if " " in keyword:
                # Multi-word: search in the full (non-deduplicated) text
                # Use word-boundary aware search so "sql" doesn't match "nosql"
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, full_text):
                    matched_keywords.append(keyword)
                    seen_matches.add(keyword)
            else:
                # Single-word: exact token match (word boundary guaranteed
                # since we split on whitespace during preprocessing)
                if keyword in token_set:
                    matched_keywords.append(keyword)
                    seen_matches.add(keyword)

        results[domain] = {
            "matched": len(matched_keywords),
            "total_keywords": len(keywords),
            "matched_keywords": matched_keywords,
        }

    return results
