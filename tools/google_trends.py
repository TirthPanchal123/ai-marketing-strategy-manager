"""Google Trends analysis tool using DuckDuckGo as fallback.

Note: pytrends was archived in April 2025. This tool uses DuckDuckGo
search to gather trend-related information as a reliable alternative.
"""

import json
from marketing_agents import function_tool
from duckduckgo_search import DDGS


@function_tool
def get_trending_topics(keyword: str) -> str:
    """
    Get trending information and related topics for a keyword.
    Searches for trend data, popular related searches, and rising topics.

    Args:
        keyword: The keyword to analyze trends for.

    Returns:
        Trend data including related searches and topic analysis.
    """
    try:
        with DDGS() as ddgs:
            # Search for trend information
            trend_results = list(ddgs.text(
                f"{keyword} trends 2025 2026 growth statistics",
                max_results=5
            ))

            # Search for related topics
            related_results = list(ddgs.text(
                f"{keyword} related topics popular searches",
                max_results=5
            ))

            # Search for market direction
            direction_results = list(ddgs.text(
                f"{keyword} market growth forecast 2026",
                max_results=3
            ))

        trend_data = {
            "keyword": keyword,
            "trend_insights": [
                {"title": r.get("title", ""), "snippet": r.get("body", "")}
                for r in trend_results
            ],
            "related_topics": [
                {"title": r.get("title", ""), "snippet": r.get("body", "")}
                for r in related_results
            ],
            "market_direction": [
                {"title": r.get("title", ""), "snippet": r.get("body", "")}
                for r in direction_results
            ],
        }

        return json.dumps(trend_data, indent=2)
    except Exception as e:
        return f"Trends error: {str(e)}"


@function_tool
def compare_trends(keywords: str) -> str:
    """
    Compare trend data for multiple keywords (comma-separated).
    Searches for comparative data between the specified keywords.

    Args:
        keywords: Comma-separated keywords to compare (max 5).

    Returns:
        Comparative trend data for the keywords.
    """
    try:
        keyword_list = [k.strip() for k in keywords.split(",")][:5]

        with DDGS() as ddgs:
            comparison_query = " vs ".join(keyword_list) + " comparison market share 2026"
            results = list(ddgs.text(comparison_query, max_results=8))

        comparison = {
            "keywords_compared": keyword_list,
            "comparison_results": [
                {
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "source": r.get("href", "")
                }
                for r in results
            ],
        }

        return json.dumps(comparison, indent=2)
    except Exception as e:
        return f"Trends comparison error: {str(e)}"
