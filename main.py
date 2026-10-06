
import csv
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from scrapers.base_scraper import create_session
from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes

from processing.cleaning import clean_text, strip_quotes, clean_price, clean_rating, clean_tags
from processing.validation import validate_record
from processing.deduplication import find_duplicates

def setup_logging():
    """Configures logging to write to both console and logs/scraper.log."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "scraper.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logger = logging.getLogger("main")
    
    start_time = time.time()
    logger.info("Starting ETL Pipeline execution.")
    
    # Create output directories
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # 1. Extraction Layer
    session = create_session()
    raw_books = scrape_books(session)
    raw_quotes = scrape_quotes(session)
    
    collected_counts = {
        "Books to Scrape": len(raw_books),
        "Quotes to Scrape": len(raw_quotes)
    }
    
    all_raw = raw_books + raw_quotes
    logger.info("Extracted %d total raw records.", len(all_raw))
    
    # 2. Transformation & Cleaning Layer
    cleaned_records = []
    for rec in all_raw:
        source = rec.get("source")
        if source == "Books to Scrape":
            cleaned_rec = {
                "source": source,
                "source_url": rec.get("source_url"),
                "name_or_title": clean_text(rec.get("name_or_title")),
                "category": clean_text(rec.get("category")),
                "price": clean_price(rec.get("price_raw")),
                "rating": clean_rating(rec.get("rating_raw")),
                "author": None,
                "tags": "",
                "description": clean_text(rec.get("description")),
                "scraped_at": rec.get("scraped_at")
            }
        else:  # Quotes to Scrape
            cleaned_rec = {
                "source": source,
                "source_url": rec.get("source_url"),
                "name_or_title": strip_quotes(rec.get("name_or_title")),
                "category": clean_text(rec.get("category")),
                "price": None,
                "rating": None,
                "author": clean_text(rec.get("author")),
                "tags": clean_tags(rec.get("tags", [])),
                "description": None,
                "scraped_at": rec.get("scraped_at")
            }
        cleaned_records.append(cleaned_rec)
        
    # 3. Validation Layer
    valid_records = []
    rejection_reasons = {}
    
    for rec in cleaned_records:
        problems = validate_record(rec)
        if problems:
            for problem in problems:
                rejection_reasons[problem] = rejection_reasons.get(problem, 0) + 1
            logger.warning("Rejected record from %s: %s | Problems: %s", rec.get("source"), rec.get("name_or_title"), problems)
        else:
            valid_records.append(rec)
            
    # 4. Deduplication Layer
    unique_records, duplicate_records = find_duplicates(valid_records)
    logger.info("Found %d unique records and %d duplicates.", len(unique_records), len(duplicate_records))
    
    # 5. Load / Save Outputs
    csv_path = output_dir / "final_dataset.csv"
    fieldnames = [
        "source", "source_url", "name_or_title", "category", 
        "price", "rating", "author", "tags", "description", "scraped_at"
    ]
    
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_records)
    logger.info("Saved final dataset to %s", csv_path)
    
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    summary_stats = {
        "collected_per_source": collected_counts,
        "rejected_by_reason": rejection_reasons,
        "duplicates_detected": len(duplicate_records),
        "final_record_count": len(unique_records),
        "duration_seconds": duration
    }
    
    json_path = output_dir / "summary_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_stats, f, indent=4)
    logger.info("Saved summary report to %s", json_path)
    logger.info("Pipeline completed successfully in %.2f seconds.", duration)

if __name__ == "__main__":
    main()