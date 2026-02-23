from app.services.suggestions import suggestion_service

def test_suggestions():
    seo_data = {
        "title": "Short",
        "meta_description": "",
        "headers": {"h1": ["Welcome", "Extra H1"]},
        "word_count": 100,
        "canonical": "",
        "og_tags": {}
    }
    score_data = {"overall_score": 30}

    suggestions = suggestion_service.generate_suggestions(seo_data, score_data)
    print(f"Suggestions: {suggestions}")

    categories = [s['category'] for s in suggestions]
    assert "Title" in categories
    assert "Meta Description" in categories
    assert "Headers" in categories
    assert "Content" in categories
    assert "Technical" in categories
    assert "Social" in categories

    # Check for specific multiple H1 issue
    h1_suggestion = next(s for s in suggestions if s['category'] == 'Headers')
    assert "Multiple H1 tags found" in h1_suggestion['issue']

    print("Suggestion service test passed!")

if __name__ == "__main__":
    test_suggestions()
