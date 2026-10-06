from processing.validation import validate_record

def test_validate_record_success():
    """A completely valid record should return an empty problems list."""
    valid_rec = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/catalogue/book-1.html",
        "name_or_title": "Python Programming",
        "price": 29.99,
        "rating": 5
    }
    assert validate_record(valid_rec) == []

def test_validate_record_failures():
    """An invalid record should flag all incorrect fields."""
    invalid_rec = {
        "source": "Invalid Source",
        "source_url": "ftp://invalid-url.com",
        "name_or_title": "",
        "price": -10.0,
        "rating": 6
    }
    problems = validate_record(invalid_rec)
    
    assert "unknown_source" in problems
    assert "missing_name" in problems
    assert "invalid_url" in problems
    assert "invalid_price" in problems
    assert "invalid_rating" in problems