from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import time
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def scrape_quotes(session: requests.Session) -> list[dict]:
    """Scrapes all quotes pages following the 'next' link dynamically."""
    start_url = "https://quotes.toscrape.com/"
    url = start_url
    page = 1
    raw_records = []
    
    while url:
        logger.info("Scraping Quotes Page %d: %s", page, url)
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
        except requests.RequestException as exc:
            logger.error("Failed to fetch quotes page %s: %s", url, exc)
            break
            
        soup = BeautifulSoup(response.text, "lxml")
        quotes = soup.select("div.quote")
        
        for quote_div in quotes:
            try:
                text_elem = quote_div.select_one("span.text")
                author_elem = quote_div.select_one("small.author")
                tag_elems = quote_div.select("div.tags > a.tag")
                
                quote_text = text_elem.get_text() if text_elem else None
                author = author_elem.get_text() if author_elem else None
                tags = [t.get_text() for t in tag_elems]
                
                raw_records.append({
                    "source": "Quotes to Scrape",
                    "source_url": url,
                    "name_or_title": quote_text,
                    "category": "Quotes",
                    "price_raw": None,
                    "rating_raw": None,
                    "author": author,
                    "tags": tags,
                    "description": None,
                    "scraped_at": datetime.now(timezone.utc).isoformat()
                })
            except Exception as e:
                logger.warning("Error parsing individual quote record: **%s**", e)
                
        # Find next page link
        next_link = soup.select_one("li.next > a")
        url = urljoin(url, next_link["href"]) if next_link else None
        page += 1
        time.sleep(0.5)
        
    return raw_records