def calculate_confidence(match_results):
    """
    Calculates confidence score (0-100%) for each domain.
    """

    confidence_results = {}

    for domain, info in match_results.items():

        matched = info["matched"]
        total = info["total_keywords"]

        # Avoid division by zero
        if total == 0:
            confidence = 0
        else:
            confidence = round((matched / total) * 100, 2)

        confidence_results[domain] = {
            "confidence": confidence,
            "matched": matched,
            "total_keywords": total,
            "matched_keywords": info["matched_keywords"]
        }

    return confidence_results