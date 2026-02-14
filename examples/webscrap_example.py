from fang.modules.scrapper import WebScraper



scraper = WebScraper("https://example.com")


scraper.fetch_page()

scraper.parse_page()


print(scraper.get_title())