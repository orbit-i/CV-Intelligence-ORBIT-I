from classifier.preprocess import preprocess_text
from classifier.keyword_matcher import keyword_match
from classifier.confidence_score import calculate_confidence


def classify_resume(resume_text):
    """
    Complete pipeline:
    Resume -> Preprocess -> Keyword Match -> Confidence -> Final Decision
    """

    # Step 1
    tokens = preprocess_text(resume_text)

    # Step 2
    match_results = keyword_match(tokens)

    # Step 3
    confidence_results = calculate_confidence(match_results)

    # Step 4: Find highest confidence domain
    best_domain = None
    best_result = None

    for domain, result in confidence_results.items():

        if best_result is None:
            best_domain = domain
            best_result = result

        elif result["confidence"] > best_result["confidence"]:
            best_domain = domain
            best_result = result

    # Step 5: Manual Review Rule
    if best_result["confidence"] >= 75:
        status = "Accepted"
    else:
        status = "Manual Review"

    return {
        "predicted_domain": best_domain,
        "confidence": best_result["confidence"],
        "status": status,
        "matched_keywords": best_result["matched_keywords"],
        "matched": best_result["matched"],
        "total_keywords": best_result["total_keywords"]
    }