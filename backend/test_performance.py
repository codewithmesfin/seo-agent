import asyncio
from unittest.mock import AsyncMock, patch
from app.services.performance import performance_service

async def test_performance_mock():
    mock_response = {
        "lighthouseResult": {
            "categories": {
                "performance": {"score": 0.95}
            },
            "audits": {
                "first-contentful-paint": {"displayValue": "1.0 s"},
                "largest-contentful-paint": {"displayValue": "1.5 s"},
                "total-blocking-time": {"displayValue": "100 ms"},
                "cumulative-layout-shift": {"displayValue": "0.01"},
                "speed-index": {"displayValue": "1.2 s"}
            }
        }
    }

    from unittest.mock import MagicMock
    mock_resp = MagicMock()
    mock_resp.json.return_value = mock_response
    mock_resp.status_code = 200
    mock_resp.raise_for_status = lambda: None

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_resp

        # Set a dummy API key for testing
        performance_service.api_key = "dummy_key"

        metrics = await performance_service.get_performance_metrics("https://example.com")
        print(f"Mocked Metrics: {metrics}")

        assert metrics["performance_score"] == 95.0
        assert metrics["first_contentful_paint"] == "1.0 s"
        print("Performance service mock test passed!")

if __name__ == "__main__":
    asyncio.run(test_performance_mock())
