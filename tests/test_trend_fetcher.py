import pytest


def test_trend_fetcher_returns_expected_structure():
    """Expect a `fetch_trends()` function that returns a list of trend dicts.

    Each trend must contain:
      - topic: str
      - score: float
      - timestamp: str (ISO8601)

    This test is intentionally written against a non-existent/empty
    implementation so it SHOULD fail until the agent implements it.
    """
    from scripts import trend_fetcher

    trends = trend_fetcher.fetch_trends()

    assert isinstance(trends, list), "trends must be a list"
    assert len(trends) > 0, "expected at least one trend (placeholder)"

    for t in trends:
        assert isinstance(t, dict)
        assert "topic" in t and isinstance(t["topic"], str)
        assert "score" in t and isinstance(t["score"], (int, float))
        assert "timestamp" in t and isinstance(t["timestamp"], str)

