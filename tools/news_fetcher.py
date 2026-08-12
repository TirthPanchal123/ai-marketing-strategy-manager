"""News fetching tool using DuckDuckGo News - No API key required."""

import json
from marketing_agents import function_tool
from duckduckgo_search import DDGS


@function_tool
def fetch_industry_news(industry: str) -> str:
    """
    Fetch recent industry news and trends.
    Use this to stay updated on industry developments and market shifts.

    Args:
        industry: The industry to search news for (e.g., 'fintech', 'e-commerce').

    Returns:
        Recent news articles about the industry.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(
                f"{industry} industry news trends 2025 2026",
                max_results=10
            ))

        if not results:
            return f"No recent news found for {industry} industry."

        articles = []
        for r in results:
            articles.append({
                "title": r.get("title", ""),
                "body": r.get("body", ""),
                "date": r.get("date", ""),
                "source": r.get("source", ""),
                "url": r.get("url", ""),
            })

        return json.dumps(articles, indent=2)
    except Exception as e:
        return f"News fetch error: {str(e)}"


@function_tool
def fetch_competitor_news(competitor_name: str) -> str:
    """
    Fetch recent news about a specific competitor company.
    Use this to monitor competitor activities and announcements.

    Args:
        competitor_name: Name of the competitor company.

    Returns:
        Recent news about the competitor.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(
                f"{competitor_name} company news announcements",
                max_results=5
            ))

        if not results:
            return f"No recent news found for {competitor_name}."

        articles = []
        for r in results:
            articles.append({
                "title": r.get("title", ""),
                "body": r.get("body", ""),
                "date": r.get("date", ""),
                "source": r.get("source", ""),
            })

        return json.dumps(articles, indent=2)
    except Exception as e:
        return f"Competitor news error: {str(e)}"
