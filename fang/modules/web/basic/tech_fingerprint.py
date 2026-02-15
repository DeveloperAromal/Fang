from fang.modules.web.basic.web_scrapper import WebScraper

class TechFingerprint:
    
    def __init__(self, url: str):
        
        self.url = url
        self.scrapper = WebScraper(url)
        
        self.data = {
            "headers": {},
            "cookies": [],
            "frontend": [],
            "backend": [],
            "meta": []
        }
        
    
    def _detect_backend(self):
        
        headers = self.data["headers"]
        
        if "Server" in headers:
            self.data["backend"].append(headers["Server"])
            
        if "X-Powered-By" in headers:
            self.data["backend"].append(headers["X-Powered-By"])
            
        for cookie in self.data["cookies"]:
            
            if "php" in cookie.lower():
                self.data["backend"].append("PHP")
                
            if "asp" in cookie.lower():
                self.data["backend"].append("ASP.NET")
    
    
    
    def _detect_meta(self):
        
        soup = self.scrapper.soup
        
        if not soup:
            return
        
        for meta in soup.findAll("meta"):
            
            if meta.get("name") == "generator":
                self.data["meta"].append(meta.get("content"))
    
    
    def _detect_frontend(self):
        
        soup = self.scrapper.soup
        
        if not soup:
            return
        
        scripts = soup.find_all("script", src=True)
        
        for script in scripts:
            
            src = script["src"].lower()
            
            if "react" in src:
                self.data["frontend"].append("React")
                
            if "vue" in src:
                self.data["frontend"].append("Vue")

            if "angular" in src:
                self.data["frontend"].append("Angular")
    
    def fingerprint(self):
        
        self.scrapper.fetch_page()
        self.scrapper.parse_page()
        
        self.data["headers"] = self.scrapper.extract_headers()
        self.data["cookies"] = self.scrapper.extract_cookies()
        
        self._detect_backend()
        self._detect_meta()
        self._detect_frontend()
        
        return self.data
