import requests

from fang.modules.web.basic.web_scrapper import *

class URLCrawler:
    
    def __init__(self, url: str):
        
        self.start_url = url
        self.visited = set()
        self.to_visit = [url]
    
    
    
    def crawl(self, max_pages = 50):
                
        while self.to_visit and len(self.visited) < max_pages:
           
            current_url = self.to_visit.pop(0)
           
            if current_url in self.visited:
               continue
           
            try:
                 
                res = requests.get(current_url, timeout = 10)
                
                if res.status_code == 200 or res.status_code == 201:
                    
                    print(f"Crawling: {current_url}")
                    self.visited.add(current_url)
                    
                    scraper = WebScraper(current_url)
                    links = scraper.get_all_links()
                    
                    for link in links:
                        if link not in self.visited:
                            self.to_visit.append(link)
                            self.to_visit.append(link)
                        
                   
                
            except requests.RequestException:
                continue
                    
        return list(self.visited)