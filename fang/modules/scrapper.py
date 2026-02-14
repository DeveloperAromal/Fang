from bs4 import BeautifulSoup

import requests


class WebScraper:
    
    def __init__(self, url):
        
        self.url = url
        self.html = None
        self.soup = None
        
        
    def fetch_page(self):
        
        response = requests.get(self.url)
        self.html = response.text
        
    
    def parse_page(self):
        
        self.soup = BeautifulSoup(self.html, "html.parser")
        
    
    def get_title(self):
        
        if self.soup:
            
            return self.soup.title.text
        
        return "Nothing found!"