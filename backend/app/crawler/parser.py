import json
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from urllib.parse import urlparse

class SEOParser:
    def __init__(self, html: str, url: str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url
        self.domain = urlparse(url).netloc

    def parse_all(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.get_title(),
            "meta_description": self.get_meta_description(),
            "headers": self.get_headers(),
            "canonical": self.get_canonical(),
            "og_tags": self.get_og_tags(),
            "robots": self.get_robots(),
            "links": self.get_links(),
            "structured_data": self.get_structured_data(),
            "word_count": self.get_word_count(),
        }

    def get_title(self) -> str:
        title = self.soup.title
        return title.string if title else ""

    def get_meta_description(self) -> str:
        meta = self.soup.find("meta", attrs={"name": "description"})
        return meta.get("content", "") if meta else ""

    def get_headers(self) -> Dict[str, List[str]]:
        headers = {}
        for i in range(1, 7):
            tag = f"h{i}"
            headers[tag] = [h.get_text().strip() for h in self.soup.find_all(tag)]
        return headers

    def get_canonical(self) -> str:
        link = self.soup.find("link", rel="canonical")
        return link.get("href", "") if link else ""

    def get_og_tags(self) -> Dict[str, str]:
        og = {}
        for meta in self.soup.find_all("meta", property=lambda p: p and p.startswith("og:")):
            og[meta.get("property")] = meta.get("content", "")
        return og

    def get_robots(self) -> str:
        meta = self.soup.find("meta", attrs={"name": "robots"})
        return meta.get("content", "") if meta else ""

    def get_links(self) -> Dict[str, List[str]]:
        internal = []
        external = []
        for a in self.soup.find_all("a", href=True):
            href = a.get("href")
            parsed = urlparse(href)
            if not parsed.netloc or parsed.netloc == self.domain:
                internal.append(href)
            else:
                external.append(href)
        return {"internal": list(set(internal)), "external": list(set(external))}

    def get_structured_data(self) -> List[Dict[str, Any]]:
        data = []
        for script in self.soup.find_all("script", type="application/ld+json"):
            try:
                data.append(json.loads(script.get_text()))
            except:
                continue
        return data

    def get_word_count(self) -> int:
        text = self.soup.get_text()
        words = text.split()
        return len(words)
