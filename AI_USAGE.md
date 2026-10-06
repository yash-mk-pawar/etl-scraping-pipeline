# AI Usage Documentation

## 1. AI Tools Utilized
- **AI Collaborator (Gemini):** Used as an interactive pair-programmer to assist with structural layout, regex patterns for price cleaning, and pipeline orchestration.

## 2. Sample Prompt
> *"Help me design a resilient HTTP session handler using requests and urllib3 with exponential backoff for status codes 429 and 5xx."*

## 3. Verification & Customization
- **Reviewed Code:** Verified that all BeautifulSoup selectors (`article.product_pod`, `div.quote`, `li.next > a`) matched our manual browser inspection in Chrome DevTools.
- **Tested Locally:** Executed unit tests via `pytest` and ran full pipeline verification from a clean environment to ensure CSV row counts matched summary metrics in `summary_report.json`.