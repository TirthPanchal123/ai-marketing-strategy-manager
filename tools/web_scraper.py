"""Web scraping tool for competitor and market analysis."""

import json
from marketing_agents import function_tool
import requests
from bs4 import BeautifulSoup


@function_tool
def scrape_website(url: str) -> str:
    """
    Scrape a website to extract key information like title, description,
    headings, and main content. Useful for competitor analysis.

    Args:
        url: The URL to scrape.

    Returns:
        Extracted website information including title, meta, headings, content.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.title.string.strip() if soup.title and soup.title.string else "N/A"

        # Extract meta description
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta_desc = meta_tag.get("content", "")

        # Extract headings
        headings = []
        for tag in ["h1", "h2", "h3"]:
            for h in soup.find_all(tag)[:5]:
                text = h.get_text(strip=True)
                if text:
                    headings.append(f"[{tag.upper()}] {text}")

        # Extract main content
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()

        text = soup.get_text(separator=" ", strip=True)[:1500]

        # Extract navigation/key links
        links = []
        for a in soup.find_all("a", href=True)[:10]:
            link_text = a.get_text(strip=True)
            if link_text and len(link_text) > 2:
                links.append(link_text)

        result = {
            "url": url,
            "title": title,
            "meta_description": meta_desc[:300],
            "headings": headings[:10],
            "content_preview": text[:1000],
            "navigation_items": links[:10],
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Scraping error for {url}: {str(e)}"
