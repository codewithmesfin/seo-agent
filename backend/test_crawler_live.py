import asyncio
from app.crawler.browser import crawler
from app.crawler.parser import SEOParser

async def test_crawler():
    url = "https://example.com"
    print(f"Testing crawler with {url}...")
    try:
        html = await crawler.get_page_content(url)
        if not html:
            print("Failed to get HTML content")
            return

        parser = SEOParser(html, url)
        data = parser.parse_all()

        print("Extracted Data:")
        print(f"Title: {data['title']}")
        print(f"Word Count: {data['word_count']}")
        print(f"Internal Links: {len(data['links']['internal'])}")

        assert "Example Domain" in data['title']
        print("Crawler and Parser work correctly!")
    finally:
        await crawler.stop()

if __name__ == "__main__":
    asyncio.run(test_crawler())
