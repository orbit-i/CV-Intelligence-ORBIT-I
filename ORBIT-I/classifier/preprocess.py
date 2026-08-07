import re

# Expanded stopwords — keep domain-relevant short words like 'r', 'c'
STOPWORDS = {
    "a", "an", "the", "and", "or", "but",
    "is", "are", "was", "were",
    "to", "of", "in", "on", "at", "for",
    "with", "by", "from", "as",
    "this", "that", "these", "those",
    "be", "been", "being",
    "have", "has", "had",
    "i", "you", "he", "she", "it", "we", "they",
    "my", "your", "our", "their",
    "also", "not", "no", "so", "if", "do",
    "use", "used", "using", "work", "worked", "working",
    "team", "company", "year", "years", "experience",
    "skills", "skill", "responsibilities", "role",
    "including", "such", "etc", "well", "various",
    "able", "good", "strong", "excellent",
    "new", "one", "two", "three", "more",
    "while", "during", "within", "across",
}

# NOTE: we intentionally keep single-letter tokens like 'r', 'c'
# because they are valid programming language names.
KEEP_SHORT = {"r", "c"}


def preprocess_text(text: str) -> list:
    """
    Cleans resume text and returns a list of meaningful tokens.

    Two outputs are produced and bundled together:
      1. token_list  – individual words (for single-word keyword matching)
      2. full_text   – lowercased, punctuation-stripped string (for
                       multi-word phrase matching inside keyword_matcher)

    Returns a dict so keyword_matcher can use both forms.
    """
    # 1. Lowercase
    text = text.lower()

    # 2. Preserve original cleaned text for multi-word matching BEFORE
    #    deduplication (deduplication would break "machine learning" if
    #    "machine" appeared earlier in the doc).
    clean_text = re.sub(r"[^a-z0-9\s]", " ", text)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    # 3. Tokenise
    tokens = clean_text.split()

    # 4. Remove stopwords — but keep intentional short tokens
    tokens = [
        w for w in tokens
        if w in KEEP_SHORT or (w not in STOPWORDS and (len(w) > 1 or w in KEEP_SHORT))
    ]

    # 5. Deduplicated list for single-word lookups (order-preserved)
    seen = set()
    unique_tokens = []
    for w in tokens:
        if w not in seen:
            unique_tokens.append(w)
            seen.add(w)

    return {
        "tokens": unique_tokens,       # deduplicated word list
        "full_text": clean_text,       # full clean string for phrase search
    }
