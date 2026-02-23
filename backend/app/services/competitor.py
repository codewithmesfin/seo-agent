from typing import Dict, Any, List

class CompetitorService:
    def compare_domains(self, base_data: Dict[str, Any], competitor_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        comparisons = []
        for comp in competitor_data:
            comparison = {
                "domain": comp.get("domain"),
                "seo_score_diff": comp.get("overall_score", 0) - base_data.get("overall_score", 0),
                "word_count_diff": comp.get("word_count", 0) - base_data.get("word_count", 0),
                "overlap_score": self.calculate_overlap(base_data, comp),
                "content_gaps": self.identify_gaps(base_data, comp)
            }
            comparisons.append(comparison)

        return {
            "competitors": comparisons,
            "summary": "Compared with {} competitors".format(len(competitor_data))
        }

    def calculate_overlap(self, base: Dict[str, Any], comp: Dict[str, Any]) -> float:
        # Simple overlap logic based on headers and title keywords
        base_words = set(base.get("title", "").lower().split())
        comp_words = set(comp.get("title", "").lower().split())

        if not base_words or not comp_words:
            return 0.0

        intersection = base_words.intersection(comp_words)
        union = base_words.union(comp_words)
        return round((len(intersection) / len(union)) * 100, 2)

    def identify_gaps(self, base: Dict[str, Any], comp: Dict[str, Any]) -> List[str]:
        gaps = []
        if comp.get("word_count", 0) > base.get("word_count", 0) + 500:
            gaps.append("Competitor has significantly more content.")

        base_h2s = set([h.lower() for h in base.get("headers", {}).get("h2", [])])
        comp_h2s = set([h.lower() for h in comp.get("headers", {}).get("h2", [])])

        unique_to_comp = comp_h2s - base_h2s
        if unique_to_comp:
            gaps.append("Competitor covers topics you missed: {}".format(list(unique_to_comp)[:3]))

        return gaps

competitor_service = CompetitorService()
