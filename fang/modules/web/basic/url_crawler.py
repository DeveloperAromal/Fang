import requests
from urllib.parse import urljoin, urlparse

from fang.modules.web.basic.web_scrapper import WebScraper


class URLCrawler:

    def __init__(self, url: str):
        self.start_url = url
        self.start_netloc = urlparse(url).netloc
        self.visited = set()
        self.to_visit = [url]

    def _normalize_link(self, base, link):
        try:
            return urljoin(base, link)
        except Exception:
            return None

    def crawl(self, max_pages=50):
        while self.to_visit and len(self.visited) < max_pages:
            current_url = self.to_visit.pop(0)

            if current_url in self.visited:
                continue

            try:
                res = requests.get(current_url, timeout=10)

                if res.status_code in (200, 201):
                    print(f"Crawling: {current_url}")
                    self.visited.add(current_url)

                    scraper = WebScraper(current_url)
                    links = scraper.get_all_links()

                    for link in links:
                        normalized = self._normalize_link(current_url, link)
                        if not normalized:
                            continue

                        # only crawl same netloc to avoid going off-site
                        if urlparse(normalized).netloc != self.start_netloc:
                            continue

                        if normalized not in self.visited and normalized not in self.to_visit:
                            self.to_visit.append(normalized)

            except requests.RequestException:
                continue

        return list(self.visited)