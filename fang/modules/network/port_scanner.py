import socket
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

class PortScanner():
    
    def __init__(self, url: str):
        self.url = url
        
        self.open_ports = []
        
    
    def _get_host(self):
        
        parsed = urlparse(self.url) 
        
        return parsed.netloc if parsed.netloc else parsed.path
    
    
    def _resolve_ip(self, host):
        return socket.gethostbyname(host)
    
    def _scan_port(self, ip, port):
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            result = sock.connect_ex((ip, port))
            
            sock.close()
            
            if result == 0:
                return port
            
        except:
            pass
        
        
    def scan(self):
            
        host = self._get_host()
        ip = self._resolve_ip(host)
            
        ports = [21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080]
            
        with ThreadPoolExecutor(max_workers=50) as executor:
                
            results = executor.map(lambda p: self._scan_port(ip, p), ports)
                
            self.open_ports = [p for p in results if p]
            
            return self.open_ports