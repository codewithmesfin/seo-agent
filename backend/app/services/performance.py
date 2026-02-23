import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
from loguru import logger

class PerformanceService:
    def __init__(self):
        self.api_key = settings.PAGESPEED_API_KEY
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    async def get_performance_metrics(self, url: str, strategy: str = "mobile") -> Optional[Dict[str, Any]]:
        params = {
            "url": url,
            "key": self.api_key,
            "strategy": strategy,
            "category": ["performance", "seo", "best-practices", "accessibility"]
        }

        if not self.api_key:
            logger.warning("PAGESPEED_API_KEY not set. Performance metrics will be mocked or limited.")
            # In a real production system, you might want to fall back to local Lighthouse
            # or return an error. For now, we'll return None or a mock if in dev.
            return None

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=60.0)
                response.raise_for_status()
                data = response.json()

                lighthouse_result = data.get("lighthouseResult", {})
                categories = lighthouse_result.get("categories", {})
                audits = lighthouse_result.get("audits", {})

                metrics = {
                    "performance_score": categories.get("performance", {}).get("score", 0) * 100,
                    "first_contentful_paint": audits.get("first-contentful-paint", {}).get("displayValue", ""),
                    "largest_contentful_paint": audits.get("largest-contentful-paint", {}).get("displayValue", ""),
                    "total_blocking_time": audits.get("total-blocking-time", {}).get("displayValue", ""),
                    "cumulative_layout_shift": audits.get("cumulative-layout-shift", {}).get("displayValue", ""),
                    "speed_index": audits.get("speed-index", {}).get("displayValue", ""),
                }
                return metrics
            except Exception as e:
                logger.error(f"Error fetching PageSpeed Insights for {url}: {str(e)}")
                return None

performance_service = PerformanceService()
