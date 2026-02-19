import whois
from urllib.parse import urlparse



class DomainDetails:
    
    def __init__(self, url: str):
        
        self.url = url
        
        self.data =  {
            "creation_date": None,
            "expiration_date": None,
            "registrar": None
        }
        
        
    def _get_domain(self):
        
        parsed = urlparse(self.url)
        domain = parsed.netloc if parsed.netloc else parsed.path
        
        return domain.replace("www.", "")    
    
    def scan(self):
        
        try:
            domain = self._get_domain()
            w = whois.whois(domain)
            
            self.data["creation_date"] = w.creation_date
            self.data["expiration_date"] = w.expiration_date
            self.data["registrar"] = w.registrar
            
            return self.data
        
        except Exception as e:
            
            pass