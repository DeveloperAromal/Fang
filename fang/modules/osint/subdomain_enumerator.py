import os
import requests
from urllib.parse import urlparse
from pathlib import Path

class SubdomainEnumerator:
    
    def __init__(self, url: str):
        
        self.url = url
        

    def create_template_url(self, domain: str):
        
        url = self.url
        
        init_domain = url.replace("http://www.", "").replace("https://www.", "").strip()
        
        protocol = urlparse(url).scheme
        
        return f"{protocol}://{domain}.{init_domain}"
        
        

    def scan_subdomain(self):
        
        BASE_DIR = Path(__file__).resolve().parents[2]
        DIR_PATH =  BASE_DIR / "data" / "subdomain_list.txt"
        
        subdomain_list_path = os.path.abspath(DIR_PATH)
        
        with open(subdomain_list_path, "r") as f:
            
            domains = f.read().splitlines()
            
            for subdomain in domains:
                
                template_url = self.create_template_url(subdomain)
                
                try:
                    res = requests.get(template_url, timeout=10)
                    
                    if res.status_code == 200 or res.status_code == 201:
                        
                        print(f"Found {subdomain}")
                        
                except requests.exceptions.RequestException as e:
                    
                    pass  
