from typing import Dict, Any

class SEOScorer:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.scores = {}

    def calculate_score(self) -> Dict[str, Any]:
        self.scores["title"] = self.score_title()
        self.scores["meta_description"] = self.score_meta_description()
        self.scores["headers"] = self.score_headers()
        self.scores["content"] = self.score_content()
        self.scores["links"] = self.score_links()
        self.scores["technical"] = self.score_technical()

        total_weight = 100
        # Weighted Average
        weights = {
            "title": 20,
            "meta_description": 15,
            "headers": 15,
            "content": 20,
            "links": 15,
            "technical": 15
        }

        overall_score = sum(self.scores[k] * (weights[k] / 100) for k in weights)
        return {
            "overall_score": round(overall_score, 2),
            "breakdown": self.scores
        }

    def score_title(self) -> float:
        title = self.data.get("title", "")
        if not title:
            return 0
        length = len(title)
        if 50 <= length <= 60:
            return 100
        elif 30 <= length <= 70:
            return 70
        else:
            return 40

    def score_meta_description(self) -> float:
        desc = self.data.get("meta_description", "")
        if not desc:
            return 0
        length = len(desc)
        if 120 <= length <= 160:
            return 100
        elif 70 <= length <= 200:
            return 70
        else:
            return 40

    def score_headers(self) -> float:
        headers = self.data.get("headers", {})
        h1s = headers.get("h1", [])
        if len(h1s) == 1:
            return 100
        elif len(h1s) > 1:
            return 50
        else:
            return 0

    def score_content(self) -> float:
        word_count = self.data.get("word_count", 0)
        if word_count > 1000:
            return 100
        elif word_count > 500:
            return 80
        elif word_count > 300:
            return 60
        else:
            return 30

    def score_links(self) -> float:
        links = self.data.get("links", {})
        internal = links.get("internal", [])
        if len(internal) > 0:
            return 100
        return 0

    def score_technical(self) -> float:
        score = 0
        if self.data.get("canonical"):
            score += 50
        if self.data.get("og_tags"):
            score += 50
        return float(score)
