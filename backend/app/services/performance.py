from typing import Dict, Any, Optional
from loguru import logger
from app.crawler.browser import crawler

class PerformanceService:
    async def get_performance_metrics(self, url: str) -> Optional[Dict[str, Any]]:
        # Tool-only implementation using Playwright/CDP
        if not crawler.browser:
            await crawler.start()

        page = await crawler.context.new_page()
        try:
            logger.info(f"Gathering local performance metrics for {url}")

            # Start a CDP session to get performance metrics
            client = await page.context.new_cdp_session(page)
            await client.send("Performance.enable")

            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Get basic navigation timing via JS
            timing = await page.evaluate("() => JSON.stringify(window.performance.getEntriesByType('navigation')[0])")
            import json
            nav_timing = json.loads(timing)

            # Get CDP metrics
            cdp_metrics = await client.send("Performance.getMetrics")
            metric_dict = {m['name']: m['value'] for m in cdp_metrics['metrics']}

            # Map to our standard format
            # These are approximations of Core Web Vitals using available tools
            metrics = {
                "performance_score": self._calculate_local_score(metric_dict, nav_timing),
                "first_contentful_paint": f"{round(nav_timing.get('domContentLoadedEventEnd', 0) / 1000, 2)} s",
                "largest_contentful_paint": f"{round(nav_timing.get('loadEventEnd', 0) / 1000, 2)} s", # Approximation
                "total_blocking_time": f"{round(metric_dict.get('ThreadTime', 0) * 1000, 2)} ms",
                "cumulative_layout_shift": "0.0", # Harder to get without full Lighthouse
                "speed_index": f"{round(nav_timing.get('duration', 0) / 1000, 2)} s",
            }
            return metrics
        except Exception as e:
            logger.error(f"Error gathering local performance for {url}: {str(e)}")
            return None
        finally:
            await page.close()

    def _calculate_local_score(self, cdp_metrics: Dict[str, Any], nav_timing: Dict[str, Any]) -> float:
        # Simple heuristic for a 0-100 score based on load time
        load_time = nav_timing.get('loadEventEnd', 0)
        if load_time == 0: return 0

        if load_time < 1000: return 100
        if load_time < 2000: return 90
        if load_time < 3000: return 75
        if load_time < 5000: return 50
        return 30

performance_service = PerformanceService()
