from bs4 import BeautifulSoup

import requests


class WebScraper:
    
    def __init__(self, url):
        
        self.url = url
        self.html = None
        self.soup = None
        self.response = None
        self.cookies = None
        self.headers = None
        
        
    def fetch_page(self):
        
       try:
           
           self.response = requests.get(self.url, timeout=10)
           self.html = self.response.text
           self.headers = self.response.headers
           self.cookies = self.response.cookies
           

       except requests.RequestException as e:
           
           pass
        
        
    
    def get_html(self):
        
       try:
           
           self.response = requests.get(self.url, timeout=10)
           self.html = self.response.text    
              
           return self.html
       
       except requests.RequestException as e:
           
           pass
       
    
    def parse_page(self):
        
        if self.html:
            
            self.soup = BeautifulSoup(self.html, "html.parser")
        
        
    def extract_headers(self):
        
        return dict(self.headers) if self.headers else {}
    
    
    
    def extract_cookies(self):
        
        if not self.cookies:
            
            return []
        
        return [cookie.name for cookie in self.cookies]
    
    
    
    
    def get_all_links(self):

        if not self.html:
            self.fetch_page()

        if not self.html:
            print("HTML is None")
            return []

        if not self.soup:
            self.parse_page()

        if not self.soup:
            print("Soup is None")
            return []

        return [a["href"] for a in self.soup.find_all("a", href=True)]
