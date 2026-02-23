import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from app.worker.tasks import async_scan

async def test_worker_task():
    url = "https://example.com"

    mock_html = "<html><title>Example Domain</title><body></body></html>"

    with patch("app.crawler.browser.crawler.get_page_content", new_callable=AsyncMock) as mock_get_content:
        mock_get_content.return_value = mock_html

        with patch("app.services.performance.performance_service.get_performance_metrics", new_callable=AsyncMock) as mock_get_perf:
            mock_get_perf.return_value = {"performance_score": 90}

            result = await async_scan(url)
            print(f"Task Result: {result.get('url')} - Score: {result.get('score', {}).get('overall_score')}")

            assert result['url'] == url
            assert result['score']['overall_score'] > 0
            assert result['performance']['performance_score'] == 90
            print("Worker task test passed!")

if __name__ == "__main__":
    asyncio.run(test_worker_task())
