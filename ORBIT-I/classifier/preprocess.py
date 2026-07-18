import re
stopwords = {
    "a", "an", "the", "and", "or", "but",
    "is", "are", "was", "were",
    "to", "of", "in", "on", "at", "for",
    "with", "by", "from", "as",
    "this", "that", "these", "those",
    "be", "been", "being",
    "have", "has", "had",
    "i", "you", "he", "she", "it", "we", "they",
    "my", "your", "our", "their"}

def preprocess_text(text: str) -> list:
    """
    Cleans resume text and returns a list of meaningful words.
    """

    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove punctuation and special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # 3. Split into individual words
    tokens = text.split()

    # 4. Remove stopwords
    tokens = [word for word in tokens if word not in stopwords]

    # 5. Remove duplicate words while preserving order
    seen = set()
    cleaned_tokens = []

    for word in tokens:
        if word not in seen:
            cleaned_tokens.append(word)
            seen.add(word)

    return cleaned_tokens