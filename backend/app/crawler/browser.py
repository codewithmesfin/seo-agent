import asyncio
from typing import Optional
from playwright.async_api import async_playwright
from loguru import logger

class Crawler:
    def __init__(self):
        self.browser = None
        self.context = None

    async def start(self):
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'pw'):
            await self.pw.stop()

    async def get_page_content(self, url: str) -> Optional[str]:
        if not self.browser:
            await self.start()

        page = await self.context.new_page()
        try:
            logger.info(f"Crawling {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            content = await page.content()
            return content
        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")
            return None
        finally:
            await page.close()

    async def crawl_domain(self, start_url: str, limit: int = 10):
        from app.crawler.parser import SEOParser
        visited = set()
        to_visit = [start_url]
        results = []

        domain = start_url.split("//")[-1].split("/")[0]

        while to_visit and len(visited) < limit:
            url = to_visit.pop(0)
            if url in visited:
                continue

            content = await self.get_page_content(url)
            if content:
                parser = SEOParser(content, url)
                data = parser.parse_all()
                results.append(data)
                visited.add(url)

                # Extract internal links for next crawls
                for link in data['links']['internal']:
                    full_link = link
                    if link.startswith("/"):
                        full_link = f"{start_url.split('//')[0]}//{domain}{link}"
                    if domain in full_link and full_link not in visited:
                        to_visit.append(full_link)

        return results

crawler = Crawler()
