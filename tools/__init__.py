"""Marketing analysis tools for AI agents."""

from tools.web_search import search_web, search_news
from tools.google_trends import get_trending_topics, compare_trends
from tools.web_scraper import scrape_website
from tools.news_fetcher import fetch_industry_news, fetch_competitor_news
from tools.seo_analyzer import analyze_seo

__all__ = [
    "search_web",
    "search_news",
    "get_trending_topics",
    "compare_trends",
    "scrape_website",
    "fetch_industry_news",
    "fetch_competitor_news",
    "analyze_seo",
]
