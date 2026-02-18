import re
from fang.modules.web.basic.web_scrapper import WebScraper

class SocialMediaDataOSINT:
    
    def __init__(self, url: str):
        
        self.url = url
        self.scraper = WebScraper(self.url)
        
        self.pattern = re.compile(r"""
            https?:\/\/
            (?:www\.)?
            (?:facebook|twitter|x|
               instagram|linkedin|
               tiktok|youtube|
               github|reddit)
            \.com\/
            [^\s]+
        """, re.VERBOSE)
    
    def _get_all_links(self):
        links = self.scraper.get_all_links()
        print(links)
        return links
        
        
    def _match_pattern(self):
        
        links = self._get_all_links()
        social_media_links = []
        
        for link in links:
            if self.pattern.search(link): 
                social_media_links.append(link)

            
        return social_media_links
    
    
    def osint(self):
        
        return self._match_pattern()
        
         
            