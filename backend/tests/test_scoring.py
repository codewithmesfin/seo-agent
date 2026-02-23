import pytest
from app.services.scoring import SEOScorer

def test_scoring_logic():
    data = {
        "title": "This is a perfect SEO title with fifty five characters!",
        "meta_description": "This is a perfect meta description that is exactly within the recommended range of one hundred and twenty to one hundred and sixty characters long for SEO.",
        "headers": {"h1": ["Welcome to the Platform"]},
        "word_count": 1200,
        "links": {"internal": ["/about"]},
        "canonical": "https://example.com",
        "og_tags": {"og:title": "Example"}
    }
    scorer = SEOScorer(data)
    result = scorer.calculate_score()
    assert result['overall_score'] == 100.0
