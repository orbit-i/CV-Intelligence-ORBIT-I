import json
import os


def load_domains():
    import sqlite3
    db_path = r"C:\Users\Admin\Desktop\orbit-I\orbit-I\data\orbit.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT domain_name, keywords FROM domains")
    rows = cursor.fetchall()
    conn.close()
    domains = {}
    for domain_name, keywords_str in rows:
        if keywords_str:
            keywords = [k.strip() for k in keywords_str.split(",")]
        else:
            keywords = []
        domains[domain_name] = keywords
    return domains


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