import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def create_session() -> requests.Session:
    """Creates a configured requests.Session with automatic retries and headers."""
    session = requests.Session()
    
    session.headers.update({
        "User-Agent": "ScrapingAssignment/1.0 (Educational Data Engineering Project)"
    })
    
    retries = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session