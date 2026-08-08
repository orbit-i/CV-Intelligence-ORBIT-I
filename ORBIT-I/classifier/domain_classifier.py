from classifier.preprocess import preprocess_text
from classifier.keyword_matcher import keyword_match
from classifier.confidence_score import calculate_confidence


def classify_resume(resume_text):
    """
    Full classification pipeline:
      Resume text
        → preprocess  (tokenise + clean, preserve full text for phrases)
        → keyword_match  (single-word + multi-word matching per domain)
        → confidence_score  (hybrid ratio + absolute + exclusivity bonus)
        → best domain selection with tie-breaking
        → manual-review threshold
    """

    # Step 1 – preprocess
    preprocessed = preprocess_text(resume_text)

    # Step 2 – keyword matching
    match_results = keyword_match(preprocessed)

    # Step 3 – confidence scoring
    confidence_results = calculate_confidence(match_results)

    # Step 4 – pick best domain with tie-breaking
    best_domain = None
    best_result = None

    for domain, result in confidence_results.items():
        if result["matched"] == 0:
            continue  # skip domains with zero hits entirely

        if best_result is None:
            best_domain = domain
            best_result = result
            continue

        current_conf = result["confidence"]
        best_conf = best_result["confidence"]

        if current_conf > best_conf:
            best_domain = domain
            best_result = result

        elif current_conf == best_conf:
            # Tie-break 1: more exclusive keyword matches wins
            if result["exclusive_matches"] > best_result["exclusive_matches"]:
                best_domain = domain
                best_result = result
            # Tie-break 2: more absolute matches wins
            elif result["exclusive_matches"] == best_result["exclusive_matches"]:
                if result["matched"] > best_result["matched"]:
                    best_domain = domain
                    best_result = result

    # Edge case: no domain matched anything
    if best_result is None:
        return {
            "predicted_domain": "Unknown",
            "confidence": 0,
            "status": "Manual Review",
            "matched_keywords": [],
            "matched": 0,
            "total_keywords": 0,
        }

    # Step 5 – threshold decision
    status = "Accepted" if best_result["confidence"] >= 75 else "Manual Review"

    return {
        "predicted_domain": best_domain,
        "confidence": best_result["confidence"],
        "status": status,
        "matched_keywords": best_result["matched_keywords"],
        "matched": best_result["matched"],
        "total_keywords": best_result["total_keywords"],
    }
