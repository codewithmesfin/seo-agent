import asyncio
from app.worker.celery_app import celery_app
from app.crawler.browser import crawler
from app.services.scoring import SEOScorer
from app.services.performance import performance_service
from app.db import init_db
from app.models.audit import Scan, Page
from loguru import logger
from datetime import datetime, timezone

@celery_app.task(name="scan_domain")
def scan_domain_task(scan_id: str, url: str):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_domain_scan(scan_id, url))

async def async_domain_scan(scan_id: str, url: str):
    await init_db()
    scan = await Scan.get(scan_id)
    if not scan:
        logger.error(f"Scan {scan_id} not found")
        return

    scan.status = "running"
    await scan.save()

    logger.info(f"Starting domain scan for {url} (ID: {scan_id})")
    try:
        # Crawl multiple pages
        pages_data = await crawler.crawl_domain(url, limit=5)

        total_score = 0
        for data in pages_data:
            scorer = SEOScorer(data)
            score_result = scorer.calculate_score()

            page = Page(
                url=data['url'] if 'url' in data else url, # Fallback
                scan_id=scan_id,
                title=data['title'],
                meta_description=data['meta_description'],
                seo_score=score_result['overall_score'],
                word_count=data['word_count'],
                data=data
            )
            await page.insert()
            total_score += score_result['overall_score']

        # Average score
        scan.overall_score = total_score / len(pages_data) if pages_data else 0
        scan.pages_count = len(pages_data)
        scan.status = "completed"
        scan.progress = 100
        scan.updated_at = datetime.now(timezone.utc)
        await scan.save()

        logger.info(f"Domain scan completed for {url}")
        return {"status": "success", "pages": len(pages_data)}
    except Exception as e:
        logger.error(f"Scan failed for {url}: {str(e)}")
        scan.status = "failed"
        await scan.save()
        return {"error": str(e)}
