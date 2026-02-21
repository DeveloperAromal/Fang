import socket
from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

class PortScanner():
    
    def __init__(self, url: str):
        self.url = url
        
        self.open_ports = []
        self.service_map = self._load_ports()
        self.ports = list(map(int, self.service_map.keys()))

        
    
    def _get_host(self):
        
        parsed = urlparse(self.url) 
        
        return parsed.netloc if parsed.netloc else parsed.path
    
    
    def _resolve_ip(self, host):
        return socket.gethostbyname(host)
    
    
    
    def _load_ports(self):
        
        BASE_DIR = Path(__file__).resolve().parents[2]
        DIR_PATH =  BASE_DIR / "data" / "ports.json"

        with open(DIR_PATH, "r") as f:
            return json.load(f)
    
    
    
    def _find_service(self, port: int):
        return self.service_map.get(str(port), "unknown")

    
    
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
            

        with ThreadPoolExecutor(max_workers=50) as executor:
                
            results = executor.map(lambda p: self._scan_port(ip, p), self.ports)
        
        open_ports = [p for p in results if p]
            
        enriched = [
            {
                "port": port,
                "service": self._find_service(port)
            }
            
            for port in open_ports
        ]       
            
            
        return {
                    "host": host,
                    "ip": ip,
                    "total_scanned": len(self.ports),
                    "open_ports_count": len(enriched),
                    "open_ports": enriched
               }
        