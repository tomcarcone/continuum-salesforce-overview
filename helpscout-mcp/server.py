#!/usr/bin/env python3
"""
HelpScout MCP Server

Exposes HelpScout Docs API content as MCP tools so Claude's
"Ask your org" feature (or any MCP client) can search and retrieve
help articles directly from your knowledge base.

Environment variables:
    HELPSCOUT_API_KEY   Your HelpScout Docs API key (required)
    PORT                HTTP port to listen on (default: 8000)
    HOST                Host to bind to (default: 0.0.0.0)
"""

import os
import httpx
from typing import Optional
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server initialisation
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="HelpScout Docs",
    instructions=(
        "This server gives you access to the organisation's HelpScout "
        "knowledge base. Use search_articles to find relevant articles, "
        "get_article to read the full content of a specific article, "
        "list_collections to browse top-level sections, and list_articles "
        "to enumerate articles within a collection."
    ),
)

HELPSCOUT_API_KEY: str = os.environ.get("HELPSCOUT_API_KEY", "")
BASE_URL = "https://docsapi.helpscout.net/v1"

# HelpScout Docs API uses HTTP Basic Auth: API key as username, "X" as password
AUTH = (HELPSCOUT_API_KEY, "X")


def _check_api_key() -> None:
    if not HELPSCOUT_API_KEY:
        raise RuntimeError(
            "HELPSCOUT_API_KEY environment variable is not set. "
            "Generate an API key at Help Scout → Your Profile → Authentication → API Keys."
        )


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_articles(
    query: str,
    collection_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> str:
    """
    Search published help articles by keyword or phrase.

    Args:
        query:         The search term (required).
        collection_id: Optionally restrict search to one collection.
        page:          Page number for paginated results (default 1).
        page_size:     Results per page, max 100 (default 20).

    Returns:
        A formatted list of matching articles with ID, title, preview, and URL.
        Use get_article(id) to retrieve the full content of any result.
    """
    _check_api_key()

    params: dict = {
        "query": query,
        "status": "published",
        "visibility": "public",
        "page": page,
        "pageSize": min(page_size, 100),
    }
    if collection_id:
        params["collectionId"] = collection_id

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            f"{BASE_URL}/search/articles",
            params=params,
            auth=AUTH,
        )
        resp.raise_for_status()
        data = resp.json()

    envelope = data.get("articles", {})
    items = envelope.get("items", [])

    if not items:
        return f'No published articles found matching "{query}".'

    total = envelope.get("count", len(items))
    current_page = envelope.get("page", page)
    total_pages = envelope.get("pages", 1)

    lines = [
        f'Found {total} article(s) matching "{query}" '
        f"(page {current_page} of {total_pages}):\n"
    ]
    for article in items:
        lines.append(f"### {article.get('name', 'Untitled')}")
        lines.append(f"- **ID:** `{article.get('id', '')}`")
        lines.append(f"- **URL:** {article.get('url', 'N/A')}")
        preview = article.get("preview", "").strip()
        if preview:
            lines.append(f"- **Preview:** {preview}")
        lines.append("")

    if current_page < total_pages:
        lines.append(f"_Call search_articles again with page={current_page + 1} for more results._")

    return "\n".join(lines)


@mcp.tool()
async def get_article(article_id: str) -> str:
    """
    Retrieve the full content of a specific help article.

    Args:
        article_id: The HelpScout article ID (obtain from search_articles or list_articles).

    Returns:
        The article title, metadata, and full body text.
    """
    _check_api_key()

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            f"{BASE_URL}/articles/{article_id}",
            auth=AUTH,
        )
        resp.raise_for_status()
        data = resp.json()

    article = data.get("article", {})
    if not article:
        return f"Article `{article_id}` not found."

    lines = [
        f"# {article.get('name', 'Untitled')}",
        "",
        f"**Status:** {article.get('status', 'unknown')}",
        f"**Public URL:** {article.get('publicUrl', 'N/A')}",
        f"**Last updated:** {article.get('updatedAt', 'N/A')}",
        f"**Views:** {article.get('viewCount', 0)}",
        "",
        "---",
        "",
        article.get("text") or "_No content available._",
    ]
    return "\n".join(lines)


@mcp.tool()
async def list_collections(page: int = 1) -> str:
    """
    List all public HelpScout documentation collections (top-level sections
    of the knowledge base).

    Args:
        page: Page number (default 1).

    Returns:
        Each collection's name, ID, description, and published article count.
        Use list_articles(collection_id) to browse articles within a collection.
    """
    _check_api_key()

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            f"{BASE_URL}/collections",
            params={"page": page, "visibility": "public", "order": "asc"},
            auth=AUTH,
        )
        resp.raise_for_status()
        data = resp.json()

    envelope = data.get("collections", {})
    items = envelope.get("items", [])

    if not items:
        return "No collections found."

    total = envelope.get("count", len(items))
    current_page = envelope.get("page", page)
    total_pages = envelope.get("pages", 1)

    lines = [f"Found {total} collection(s) (page {current_page} of {total_pages}):\n"]
    for col in items:
        lines.append(f"### {col.get('name', 'Untitled')}")
        lines.append(f"- **ID:** `{col.get('id', '')}`")
        lines.append(f"- **Published articles:** {col.get('publishedArticleCount', 0)}")
        desc = col.get("description", "").strip()
        if desc:
            lines.append(f"- **Description:** {desc}")
        lines.append(f"- **URL:** {col.get('publicUrl', 'N/A')}")
        lines.append("")

    return "\n".join(lines)


@mcp.tool()
async def list_articles(
    collection_id: str,
    page: int = 1,
    page_size: int = 50,
) -> str:
    """
    List all published articles within a specific HelpScout collection.

    Args:
        collection_id: The collection ID (from list_collections).
        page:          Page number (default 1).
        page_size:     Results per page, max 100 (default 50).

    Returns:
        Article names, IDs, and URLs. Use get_article(id) to read full content.
    """
    _check_api_key()

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            f"{BASE_URL}/collections/{collection_id}/articles",
            params={
                "page": page,
                "status": "published",
                "pageSize": min(page_size, 100),
                "sort": "name",
                "order": "asc",
            },
            auth=AUTH,
        )
        resp.raise_for_status()
        data = resp.json()

    envelope = data.get("articles", {})
    items = envelope.get("items", [])

    if not items:
        return f"No published articles found in collection `{collection_id}`."

    total = envelope.get("count", len(items))
    current_page = envelope.get("page", page)
    total_pages = envelope.get("pages", 1)

    lines = [
        f"Found {total} article(s) in collection `{collection_id}` "
        f"(page {current_page} of {total_pages}):\n"
    ]
    for article in items:
        lines.append(f"- **{article.get('name', 'Untitled')}**")
        lines.append(f"  ID: `{article.get('id', '')}`  |  URL: {article.get('publicUrl', 'N/A')}")

    if current_page < total_pages:
        lines.append(
            f"\n_Call list_articles again with page={current_page + 1} for more results._"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "streamable-http")
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))

    if transport == "stdio":
        # Useful for local testing with the MCP Inspector
        mcp.run(transport="stdio")
    else:
        # Remote HTTP transport — required for Claude's "Ask your org" connector
        mcp.run(
            transport="streamable-http",
            host=host,
            port=port,
            path="/mcp",
        )
