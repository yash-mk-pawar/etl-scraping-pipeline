import hashlib
import re

def make_fingerprint(rec: dict) -> str:
    """Generates a unique cryptographic hash fingerprint for duplicate detection."""
    if rec.get("source") == "Books to Scrape":
        key = f"{rec.get('source', '')}{rec.get('name_or_title', '')}"
    else:  # Quotes to Scrape
        key = f"{rec.get('source', '')}{rec.get('author', '')}{str(rec.get('name_or_title', ''))[:50]}"
    
    # Lowercase, strip punctuation, and collapse spaces
    key = re.sub(r"[^\w\s]", "", key.lower())
    key = " ".join(key.split())
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def find_duplicates(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """Separates a list of records into unique items and duplicate items."""
    seen = set()
    unique = []
    dupes = []
    
    for rec in records:
        fp = make_fingerprint(rec)
        if fp in seen:
            dupes.append(rec)
        else:
            seen.add(fp)
            unique.append(rec)
            
    return unique, dupes