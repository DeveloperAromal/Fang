import requests
from urllib.parse import urlparse
from pathlib import Path
from typing import List

class SubdomainEnumerator:
    
    def __init__(self, url: str, timeout: int = 5):
        
        self.url = url
        self.timeout = timeout
        self.protocol = urlparse(self.url).scheme or "https"
        self.base_domain = self._extract_domain()
        
        
    def _extract_domain(self) -> str:
        
        parsed = urlparse(self.url)
        return parsed.netloc.replace("www.", "")



    def create_template_url(self, subdomain: str) -> str:
        return f"{self.protocol}://{subdomain}.{self.base_domain}"
        
    
    def _load_wordlist(self) -> List[str]:
        
        BASE_DIR = Path(__file__).resolve().parents[3]
        DIR_PATH =  BASE_DIR / "data" / "subdomain_list.txt"

        with open(DIR_PATH, "r") as f:
            
            return [line.strip() for line in f if line.strip()]

    
    
    def scan(self) -> List[str]:
        
        subdomains = self._load_wordlist()
        found_subdomains = []

        for domain in subdomains:
            
            url = self.create_template_url(domain)
            
            try:

                res = requests.get(url, timeout = self.timeout)

                if res.status_code == 200 or res.status_code == 201:
                    
                    found_subdomains.append(domain)

                    print(f"[+] Found ({len(found_subdomains)}) {domain}")
                    
                        
                        
            except requests.exceptions.RequestException as e:
                    
                continue  
            
        return found_subdomains