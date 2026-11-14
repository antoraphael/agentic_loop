import json
import logging

from ddgs import DDGS
logger = logging.getLogger(__name__)


def web_search(query: str) -> str:
    """Search the web and return a compact set of results as JSON text."""
    try:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("A non-empty search query is required.")

        results = DDGS().text(query, max_results=5)
        cleaned_results = [
            {
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", ""),
            }
            for result in results
        ]

        return json.dumps(
            {"query": query, "results": cleaned_results},
            ensure_ascii=False,
        )
    except Exception as error:
        logger.exception("Web search failed")
        return json.dumps({"error": f"Web search failed: {error}"})

