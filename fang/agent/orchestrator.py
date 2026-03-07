from fang.modules.network.port_scanner import PortScanner
from fang.modules.network.capture_banner import CaptureBanner
from fang.modules.web.basic.robots_parser import RobotsParser
from fang.modules.web.basic.subdomain_enumerator import SubdomainEnumerator
from fang.modules.web.basic.tech_fingerprint import TechFingerprint
from fang.modules.web.basic.url_crawler import URLCrawler
from fang.modules.web.basic.web_scrapper import WebScraper
from fang.modules.web.osint.domain_details import DomainDetails
from fang.modules.web.osint.social_media_data_extracter import SocialMediaDataOSINT

from fang.memory.storage import STORAGE

class Executor:

    def __init__(self, target: str):
        self.target = target
        self.scraper = WebScraper(target)
        self.port_scanner = PortScanner(target)
        self.robots = RobotsParser(target)
        self.subdomain_enum = SubdomainEnumerator(target)
        self.tech_fingerprint = TechFingerprint(target)
        self.url_mapper = URLCrawler(target)
        self.domain_details = DomainDetails(target)
        self.socialmedia_osint = SocialMediaDataOSINT(target)

    def _banner_grab(self):
        scan_result = STORAGE.get("port_scan", {})
        open_ports = [p['port'] for p in scan_result.get("open_ports", [])]

        banners = {}
        for port in open_ports:
            try:
                banners[port] = CaptureBanner(scan_result['host'], port).grab()
            except Exception as e:
                banners[port] = {"error": str(e)}

        STORAGE["banners"] = banners
        return banners


    def _tools(self):
        """Call each tool and store results in STORAGE"""
        
        STORAGE["port_scan"] = self.port_scanner.scan()
        STORAGE["robots_txt"] = self.robots.parse()
        STORAGE["subdomains"] = self.subdomain_enum.scan()
        STORAGE["tech_fingerprint"] = self.tech_fingerprint.fingerprint()
        # STORAGE["url_map"] = self.url_mapper.crawl()
        STORAGE["web_scrape"] = self.scraper.get_html()
        STORAGE["domain_details"] = self.domain_details.scan()
        # STORAGE["social_media_osint"] = self.socialmedia_osint.osint()
        STORAGE["banners"] = self._banner_grab()
        
        
        
    def run(self):
        
        self._tools()
        print(STORAGE)