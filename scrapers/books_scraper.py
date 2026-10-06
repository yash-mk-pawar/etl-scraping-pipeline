from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import time
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def scrape_books(session: requests.Session) -> list[dict]:
    """Scrapes all books pages following the 'next' link dynamically."""
    start_url = "https://books.toscrape.com/catalogue/page-1.html"
    url = start_url
    page = 1
    raw_records = []
    
    while url:
        logger.info("Scraping Books Page %d: %s", page, url)
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
        except requests.RequestException as exc:
            logger.error("Failed to fetch books page %s: %s", url, exc)
            break
            
        soup = BeautifulSoup(response.text, "lxml")
        articles = soup.select("article.product_pod")
        
        for article in articles:
            try:
                link = article.select_one("h3 > a")
                price = article.select_one("p.price_color")
                rating = article.select_one("p.star-rating")
                
                title = link.get("title") if link else None
                detail_url = urljoin(url, link["href"]) if link and link.get("href") else None
                price_raw = price.get_text() if price else None
                rating_raw = " ".join(rating.get("class", [])) if rating else None
                
                raw_records.append({
                    "source": "Books to Scrape",
                    "source_url": detail_url,
                    "name_or_title": title,
                    "category": None,      # Can be left empty or expanded if visiting detail pages
                    "price_raw": price_raw,
                    "rating_raw": rating_raw,
                    "author": None,
                    "tags": [],
                    "description": None,
                    "scraped_at": datetime.now(timezone.utc).isoformat()
                })
            except Exception as e:
                logger.warning("Error parsing individual book record: %s", e)
                
        # Find next page link
        next_link = soup.select_one("li.next > a")
        url = urljoin(url, next_link["href"]) if next_link else None
        page += 1
        time.sleep(0.5)  # Be polite to the server
        
    return raw_records