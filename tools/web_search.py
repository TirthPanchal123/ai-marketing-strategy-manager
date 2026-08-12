"""Web search tool using DuckDuckGo - No API key required."""

from marketing_agents import function_tool
from duckduckgo_search import DDGS


@function_tool
def search_web(query: str) -> str:
    """
    Search the web for information using DuckDuckGo.
    Use this to find market data, industry info, competitor details, etc.

    Args:
        query: The search query string.

    Returns:
        Search results as formatted text with titles, snippets and URLs.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=8))

        if not results:
            return "No results found for the query."

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"{i}. **{r.get('title', 'N/A')}**\n"
                f"   {r.get('body', 'N/A')}\n"
                f"   Source: {r.get('href', 'N/A')}"
            )

        return "\n\n".join(formatted)
    except Exception as e:
        return f"Search error: {str(e)}"


@function_tool
def search_news(query: str) -> str:
    """
    Search for recent news articles using DuckDuckGo News.
    Use this for latest industry news, competitor announcements, market updates.

    Args:
        query: The news search query.

    Returns:
        News results with titles, summaries, dates and sources.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=8))

        if not results:
            return "No news found for the query."

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"{i}. **{r.get('title', 'N/A')}**\n"
                f"   {r.get('body', 'N/A')}\n"
                f"   Date: {r.get('date', 'N/A')}\n"
                f"   Source: {r.get('source', 'N/A')}"
            )

        return "\n\n".join(formatted)
    except Exception as e:
        return f"News search error: {str(e)}"
