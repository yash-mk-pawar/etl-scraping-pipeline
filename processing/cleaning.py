import re

RATING_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5
}

def clean_text(value: str) -> str | None:
    """Removes extra spaces, tabs, newlines, and non-breaking spaces."""
    if value is None:
        return None
    text = " ".join(value.replace("\xa0", " ").split())
    return text or None

def strip_quotes(value: str) -> str | None:
    """Removes curly or straight quotation marks surrounding text."""
    cleaned = clean_text(value)
    if not cleaned:
        return None
    # Strip leading/trailing quote characters
    return cleaned.strip('“”"\'')

def clean_price(raw: str) -> float | None:
    """Extracts numeric price from currency strings like £51.77."""
    if not raw:
        return None
    match = re.search(r"\d+(?:\.\d+)?", raw.replace(",", ""))
    return float(match.group()) if match else None

def clean_rating(raw: str) -> int | None:
    """Converts word ratings like 'Three' into integers (1-5)."""
    for word in (raw or "").lower().split():
        if word in RATING_MAP:
            return RATING_MAP[word]
    return None

def clean_tags(tags_list: list[str]) -> str:
    """Lowercases, sorts, and joins tags with semicolons."""
    cleaned = sorted({clean_text(tag).lower() for tag in tags_list if clean_text(tag)})
    return ";".join(cleaned)