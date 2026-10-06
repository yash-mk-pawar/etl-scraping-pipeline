from processing.cleaning import clean_text, clean_price, clean_rating, strip_quotes
from processing.validation import validate_record
from processing.deduplication import find_duplicates, make_fingerprint

def test_clean_text():
    assert clean_text("  Hello \n World \xa0") == "Hello World"
    assert clean_text(None) is None

def test_strip_quotes():
    assert strip_quotes("“To be or not to be”") == "To be or not to be"

def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price(None) is None

def test_clean_rating():
    assert clean_rating("star-rating Three") == 3
    assert clean_rating("star-rating Five") == 5

def test_validation():
    valid_rec = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/catalogue/book.html",
        "name_or_title": "Test Book",
        "price": 10.99,
        "rating": 4
    }
    assert validate_record(valid_rec) == []
    
    invalid_rec = {
        "source": "Unknown Site",
        "source_url": "not-a-url",
        "name_or_title": "",
        "price": -5
    }
    problems = validate_record(invalid_rec)
    assert "unknown_source" in problems
    assert "missing_name" in problems
    assert "invalid_url" in problems
    assert "invalid_price" in problems

def test_deduplication():
    base = {"source": "Books to Scrape", "author": None, "source_url": "https://books.toscrape.com"}
    records = [
        {**base, "name_or_title": "Python 101"},
        {**base, "name_or_title": "  Python 101 "},
        {**base, "name_or_title": "PYTHON 101"}
    ]
    unique, dupes = find_duplicates(records)
    assert len(unique) == 1
    assert len(dupes) == 2