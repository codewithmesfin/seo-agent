from app.services.competitor import competitor_service

def test_competitor_comparison():
    base_data = {
        "domain": "mysite.com",
        "overall_score": 85,
        "word_count": 600,
        "title": "Best SEO Audit Tool for SaaS",
        "headers": {"h2": ["Features", "Pricing"]}
    }

    competitors = [
        {
            "domain": "competitor.com",
            "overall_score": 90,
            "word_count": 1200,
            "title": "Top SEO Audit and Competitor Analysis Tool",
            "headers": {"h2": ["Features", "Pricing", "AI Optimization", "Case Studies"]}
        }
    ]

    result = competitor_service.compare_domains(base_data, competitors)
    print(f"Comparison Result: {result}")

    comp = result['competitors'][0]
    assert comp['seo_score_diff'] == 5
    assert comp['word_count_diff'] == 600
    assert "Competitor has significantly more content." in comp['content_gaps']
    assert any("topics you missed" in gap for gap in comp['content_gaps'])
    print("Competitor service test passed!")

if __name__ == "__main__":
    test_competitor_comparison()
