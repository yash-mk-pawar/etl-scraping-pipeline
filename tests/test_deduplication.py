from processing.deduplication import make_fingerprint, find_duplicates

def test_make_fingerprint_books():
    """Fingerprints for books should be consistent despite case/whitespace differences."""
    rec1 = {"source": "Books to Scrape", "name_or_title": "Test Book Title"}
    rec2 = {"source": "Books to Scrape", "name_or_title": "  TEST BOOK TITLE! "}
    
    assert make_fingerprint(rec1) == make_fingerprint(rec2)

def test_find_duplicates():
    """Duplicates finder should accurately separate unique items from duplicate items."""
    base = {"source": "Quotes to Scrape", "author": "Albert Einstein", "source_url": "https://quotes.toscrape.com"}
    records = [
        {**base, "name_or_title": "Imagination is more important than knowledge."},
        {**base, "name_or_title": "  Imagination is more important than knowledge. "},
        {**base, "name_or_title": "Different quote text entirely."}
    ]
    
    unique, dupes = find_duplicates(records)
    assert len(unique) == 2
    assert len(dupes) == 1