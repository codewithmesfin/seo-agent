from typing import Dict, Any, List

class SuggestionService:
    def generate_suggestions(self, seo_data: Dict[str, Any], score_data: Dict[str, Any]) -> List[Dict[str, str]]:
        suggestions = []

        # Title suggestions
        title = seo_data.get("title", "")
        if not title:
            suggestions.append({
                "category": "Title",
                "issue": "Missing title tag",
                "suggestion": "Add a descriptive title tag between 50-60 characters."
            })
        elif len(title) < 30 or len(title) > 70:
            suggestions.append({
                "category": "Title",
                "issue": f"Title length is suboptimal ({len(title)} chars)",
                "suggestion": "Adjust title to be between 50-60 characters for better visibility in SERPs."
            })

        # Meta description suggestions
        desc = seo_data.get("meta_description", "")
        if not desc:
            suggestions.append({
                "category": "Meta Description",
                "issue": "Missing meta description",
                "suggestion": "Add a meta description between 120-160 characters to improve click-through rate."
            })
        elif len(desc) < 70 or len(desc) > 200:
            suggestions.append({
                "category": "Meta Description",
                "issue": f"Meta description length is suboptimal ({len(desc)} chars)",
                "suggestion": "Keep meta description between 120-160 characters."
            })

        # Header suggestions
        headers = seo_data.get("headers", {})
        h1s = headers.get("h1", [])
        if len(h1s) == 0:
            suggestions.append({
                "category": "Headers",
                "issue": "Missing H1 tag",
                "suggestion": "Ensure each page has exactly one H1 tag containing your primary keyword."
            })
        elif len(h1s) > 1:
            suggestions.append({
                "category": "Headers",
                "issue": "Multiple H1 tags found",
                "suggestion": "Use only one H1 tag per page for better document structure."
            })

        # Content suggestions
        word_count = seo_data.get("word_count", 0)
        if word_count < 300:
            suggestions.append({
                "category": "Content",
                "issue": "Thin content",
                "suggestion": "Increase word count to at least 600-1000 words for better ranking potential."
            })

        # Technical suggestions
        if not seo_data.get("canonical"):
            suggestions.append({
                "category": "Technical",
                "issue": "Missing canonical tag",
                "suggestion": "Add a canonical tag to prevent duplicate content issues."
            })

        if not seo_data.get("og_tags"):
            suggestions.append({
                "category": "Social",
                "issue": "Missing OpenGraph tags",
                "suggestion": "Add OG tags (og:title, og:description) to improve social media sharing appearance."
            })

        return suggestions

suggestion_service = SuggestionService()
