"""SEO analysis tool using web scraping - No API key required."""

import json
import re
from marketing_agents import function_tool
import requests
from bs4 import BeautifulSoup


def _calculate_seo_score(
    title_len: int,
    desc_len: int,
    h1_count: int,
    imgs_no_alt: int,
    total_imgs: int,
    og_count: int,
) -> int:
    """Calculate a simple SEO score out of 100."""
    score = 0

    # Title tag (20 pts)
    if 30 <= title_len <= 60:
        score += 20
    elif title_len > 0:
        score += 10

    # Meta description (20 pts)
    if 120 <= desc_len <= 160:
        score += 20
    elif desc_len > 0:
        score += 10

    # H1 tag (20 pts)
    if h1_count == 1:
        score += 20
    elif h1_count > 0:
        score += 10

    # Image alt text (20 pts)
    if total_imgs > 0:
        alt_ratio = (total_imgs - imgs_no_alt) / total_imgs
        score += int(20 * alt_ratio)
    else:
        score += 20

    # Open Graph tags (20 pts)
    if og_count >= 3:
        score += 20
    elif og_count > 0:
        score += 10

    return score


@function_tool
def analyze_seo(url: str) -> str:
    """
    Perform basic SEO analysis on a website.
    Checks title, meta description, headings, images, links, and OG tags.

    Args:
        url: The website URL to analyze.

    Returns:
        SEO analysis results with scores and recommendations.
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

        # Title analysis
        title = soup.title.string.strip() if soup.title and soup.title.string else "MISSING"
        title_length = len(title) if title != "MISSING" else 0
        title_status = "✅ Good" if 30 <= title_length <= 60 else "⚠️ Needs improvement"

        # Meta description
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            meta_desc = meta_tag.get("content", "")
        desc_length = len(meta_desc)
        desc_status = (
            "✅ Good" if 120 <= desc_length <= 160
            else ("❌ Missing" if desc_length == 0 else "⚠️ Needs improvement")
        )

        # Heading structure
        headings = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f"h{i}")
            if h_tags:
                headings[f"h{i}"] = {
                    "count": len(h_tags),
                    "texts": [h.get_text(strip=True)[:80] for h in h_tags[:3]],
                }

        h1_count = len(soup.find_all("h1"))
        h1_status = "✅ Good" if h1_count == 1 else f"⚠️ Found {h1_count} H1 tags"

        # Images without alt
        images = soup.find_all("img")
        images_without_alt = sum(1 for img in images if not img.get("alt"))
        img_status = (
            "✅ Good" if images_without_alt == 0
            else f"⚠️ {images_without_alt}/{len(images)} missing alt text"
        )

        # Links analysis
        internal_links = 0
        external_links = 0
        domain = url.split("/")[2] if len(url.split("/")) > 2 else ""
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http") and domain not in href:
                external_links += 1
            elif href.startswith("/") or href.startswith("#") or domain in href:
                internal_links += 1

        # Canonical URL
        canonical = soup.find("link", attrs={"rel": "canonical"})
        canonical_url = canonical.get("href", "") if canonical else "Not set"

        # Open Graph tags
        og_tags = {}
        for tag in soup.find_all("meta", attrs={"property": re.compile(r"^og:")}):
            og_tags[tag.get("property", "")] = tag.get("content", "")[:100]

        seo_score = _calculate_seo_score(
            title_length, desc_length, h1_count,
            images_without_alt, len(images), len(og_tags)
        )

        result = {
            "url": url,
            "seo_score": f"{seo_score}/100",
            "title": {"text": title[:100], "length": title_length, "status": title_status},
            "meta_description": {
                "text": meta_desc[:200],
                "length": desc_length,
                "status": desc_status,
            },
            "h1_status": h1_status,
            "heading_structure": headings,
            "images": {"total": len(images), "alt_status": img_status},
            "links": {"internal": internal_links, "external": external_links},
            "canonical": canonical_url,
            "open_graph_tags": len(og_tags),
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return f"SEO analysis error: {str(e)}"
