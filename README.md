# ETL Scraper Pipeline - Realisieren Technologies Assignment

## Project Overview
This project implements a robust ETL (Extract, Transform, Load) data pipeline in Python to collect, clean, validate, and deduplicate records from two static target websites:
1. **[Books to Scrape](https://books.toscrape.com/)** (~1,000 records across 50 pages)
2. **[Quotes to Scrape](https://quotes.toscrape.com/)** (100 records across 10 pages)

## Tech Stack
- **Python** (3.10 – 3.12)
- **Requests** (HTTP networking with resilient session retries)
- **BeautifulSoup4 & lxml** (HTML parsing)
- **Pytest** (Unit testing)

---

## Project Structure
```text
scraping_assignment/
├── scrapers/          # Networking & site-specific extraction
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
├── processing/        # Pure transformation, validation, deduplication
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
├── tests/             # Unit tests (run without internet)
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
├── output/            # Generated CSV and JSON reports
├── logs/              # Execution logs
├── main.py            # Orchestrator
└── requirements.txt