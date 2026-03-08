from fang.modules.basic.web_scrapper import WebScraper
from fang.utils.logger import Logger


scraper = WebScraper("https://example.com")


scraper.fetch_page()

scraper.parse_page()


Logger.info(scraper.get_title())