
import requests
from fang.modules.web.basic.web_scrapper import WebScraper

class RobotsParser:
    
    def __init__(self, url: str):
        
        self.url = url.rstrip("/")
        self.has_robot = self._has_robot()
        self.scrapper = WebScraper(self.url)
        
        self.data = {
            "user-agents": [],
            "allowed": [],
            "disallowed": [],
            "sitemap": []
        }
        
    
    def _has_robot(self):
        
        url = f"{self.url}/robots.txt"
        
        res = requests.get(url, timeout = 10)
        
        if res.status_code in (200, 201):
            
            return True
        
        else:
            
            return False
        
        
    def _extract_robots(self):
        
        if self.has_robot:
            
            url = f"{self.url}/robots.txt"
             
            try:
                
                robots = requests.get(url).text     
                lines = robots.splitlines()
                
                for line in lines:
                    
                    if "User-agent" in line or "user-agent" in line:
                        
                        self.data["user-agents"].append(
                            line.replace("User-agent:", "").replace("user-agent:", "")
                            )
                    
                    
                    if "Allow" in line or "allow" in line:
                            
                        self.data["allowed"].append(
                            line.replace("Allow:", "").replace("allow:", "")
                            )
                    
                    
                    if "Disallow" in line or "disallow" in line:
                        
                        if "# Disallow" in line:
                            
                            continue
                        
                        self.data["disallowed"].append(
                            line.replace("Disallow:", "").replace("disallow:", "")
                            )
                    
                    
                    if "Sitemap" in line or "sitemap" in line:
                        
                        if "# Sitemaps" in line:
                            
                            continue
                        
                        self.data["sitemap"].append(
                            line.replace("Sitemap:", "").replace("sitemap:", "")
                            )
                        
                        
            except requests.RequestException as e:
                
                pass
    
    
    def parse(self):
        
        self._extract_robots()
        
        return self.data    
        