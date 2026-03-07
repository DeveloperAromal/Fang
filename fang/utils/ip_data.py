import requests


class IPData:
    
    @staticmethod
    def ipv4():
        
        try:
            
            ip = requests.get("https://api.ipify.org?format=json", timeout = 5)
            
            return ip.json()["ip"]
        
        except requests.RequestException:
            pass
        
    @staticmethod
    def ipv6():
            
        try:
                
            ip = requests.get("https://api64.ipify.org?format=json", timeout = 5)
                
            return ip.json()["ip"]
            
        except requests.RequestException:
            pass
            
        
        