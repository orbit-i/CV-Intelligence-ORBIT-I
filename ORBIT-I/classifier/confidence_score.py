def calculate_confidence(match_results):
    """
    Calculates confidence score (0-100%) for each domain using a hybrid scoring model:

    - Raw ratio alone is unreliable: a domain with 100 keywords matching 5 scores 5%,
      while a domain with 10 keywords matching 3 scores 30% — even if it's wrong.
    - Fix: combine absolute match count (rewarding more hits) with match ratio
      (rewarding precision), weighted 60/40.
    - Exclusive keyword bonus: keywords matched that NO other domain shares get a
      +2 point bonus each, rewarding domain-specific language.
    """

    # First pass: collect all matched keywords across domains so we can
    # identify which ones are exclusive to a single domain.
    all_matched = {}
    for domain, info in match_results.items():
        for kw in info["matched_keywords"]:
            all_matched.setdefault(kw, []).append(domain)

    exclusive_keywords = {kw for kw, domains in all_matched.items() if len(domains) == 1}

    # Second pass: compute the actual score
    confidence_results = {}

    for domain, info in match_results.items():
        matched = info["matched"]
        total = info["total_keywords"]

        if total == 0 or matched == 0:
            confidence_results[domain] = {
                "confidence": 0,
                "matched": matched,
                "total_keywords": total,
                "matched_keywords": info["matched_keywords"],
                "exclusive_matches": 0,
            }
            continue

        # Component 1 – match ratio (precision): what % of this domain's
        # keywords were found in the CV?  Capped at 100.
        ratio_score = min((matched / total) * 100, 100)

        # Component 2 – absolute match score: log-scaled so each extra
        # match matters less once you already have many hits (diminishing
        # returns). Normalised to a 0-100 range assuming 20 matches ≈ max.
        import math
        abs_score = min((math.log1p(matched) / math.log1p(20)) * 100, 100)

        # Weighted blend: ratio matters more for small keyword sets,
        # abs count matters more for large sets.
        base_score = (ratio_score * 0.5) + (abs_score * 0.5)

        # Exclusive keyword bonus (up to +15 points)
        exclusive_count = sum(
            1 for kw in info["matched_keywords"] if kw in exclusive_keywords
        )
        exclusivity_bonus = min(exclusive_count * 2, 15)

        final_score = min(round(base_score + exclusivity_bonus, 2), 100)

        confidence_results[domain] = {
            "confidence": final_score,
            "matched": matched,
            "total_keywords": total,
            "matched_keywords": info["matched_keywords"],
            "exclusive_matches": exclusive_count,
        }

    return confidence_results
