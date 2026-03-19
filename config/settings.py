from fang.modules.network.port_scanner import PortScanner
from fang.modules.network.capture_banner import CaptureBanner
from fang.modules.web.basic.robots_parser import RobotsParser
from fang.modules.web.basic.subdomain_enumerator import SubdomainEnumerator
from fang.modules.web.basic.tech_fingerprint import TechFingerprint
from fang.modules.web.basic.url_crawler import URLCrawler
from fang.modules.web.basic.web_scrapper import WebScraper
from fang.modules.web.osint.domain_details import DomainDetails
from fang.modules.web.osint.social_media_data_extracter import SocialMediaDataOSINT


VERSION = "1.0.2"

IS_NEW = False

LLM_PROVIDER = ""         
LLM_API_KEY = ""
LLM_MODEL = "gemini-2.5-flash"   
LLM_MAX_TOKENS = 4096
LLM_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

TOOLS_AVAILABLE = [
    {
        "name": "scan_ports",
        "description": "Scan open ports of a target. Returns open ports, protocols, and service info.",
        "storage_key": "port_scan",
        "executor": lambda target, storage: PortScanner(target).scan(),
    },
    {
        "name": "grab_banners",
        "description": "Grab banners from open ports to identify running services and versions. Requires port scan to run first.",
        "storage_key": "banners",
        "executor": None, 
        "depends_on": "scan_ports",
    },
    {
        "name": "parse_robots",
        "description": "Parse robots.txt of a target. Reveals disallowed paths and hidden endpoints.",
        "storage_key": "robots_txt",
        "executor": lambda target, storage: RobotsParser(target).parse(),
    },
    {
        "name": "enumerate_subdomains",
        "description": "Enumerate subdomains of a target using a wordlist. Expands the attack surface.",
        "storage_key": "subdomains",
        "executor": lambda target, storage: SubdomainEnumerator(target).scan(),
    },
    {
        "name": "fingerprint_tech",
        "description": "Fingerprint web technologies used by the target (CMS, frameworks, servers, JS libraries).",
        "storage_key": "tech_fingerprint",
        "executor": lambda target, storage: TechFingerprint(target).fingerprint(),
    },
    {
        "name": "crawl_urls",
        "description": "Crawl URLs from the target website. Maps endpoints and discovers hidden pages.",
        "storage_key": "url_map",
        "executor": lambda target, storage: URLCrawler(target).crawl(),
    },
    {
        "name": "scrape_web",
        "description": "Scrape raw HTML content from the target. Useful for finding comments, metadata, and exposed data.",
        "storage_key": "web_scrape",
        "executor": lambda target, storage: WebScraper(target).get_html(),
    },
    {
        "name": "domain_details",
        "description": "Get OSINT domain details including WHOIS, registrar, DNS records, and IP info.",
        "storage_key": "domain_details",
        "executor": lambda target, storage: DomainDetails(target).scan(),
    },
    {
        "name": "social_media_osint",
        "description": "Extract social media presence and data linked to the target domain or organization.",
        "storage_key": "social_media_osint",
        "executor": lambda target, storage: SocialMediaDataOSINT(target).osint(),
    },
]


def grab_banners_executor(target, storage):
    port_scan = storage.get("port_scan") or {}

    host = port_scan.get("host") or target

    open_ports = port_scan.get("open_ports", [])

    if not open_ports:
        return []

    results = []
    for entry in open_ports:
        port = entry.get("port")
        try:
            res = CaptureBanner(host, port).grab()
            results.append(res)
        except Exception as e:
            results.append({"host": host, "port": port, "error": str(e)})

    return results


for t in TOOLS_AVAILABLE:
    if t.get("name") == "grab_banners":
        t["executor"] = grab_banners_executor
        break
    
    
def get_api_key() -> str:
    with open("config/settings.py", "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("LLM_API_KEY") and "=" in stripped:
                _, _, value = stripped.partition("=")
                return value.strip().strip('"').strip("'")
    return ""


TARGET = ""                         
SCAN_TIMEOUT = 5                    
MAX_THREADS = 10                    

PORT_SCAN_RANGE = (1, 1024)         
PORT_SCAN_TOP_PORTS_ONLY = True     


SUBDOMAIN_WORDLIST = "fang/data/subdomain_list.txt"
SUBDOMAIN_THREADS = 20


USER_AGENT = "Mozilla/5.0 (compatible; Fang-Scanner/1.0)"
MAX_CRAWL_DEPTH = 2
MAX_CRAWL_PAGES = 50
RESPECT_ROBOTS_TXT = False          


REPORT_OUTPUT_DIR = "generated"
REPORT_FORMAT = "markdown"         
REPORT_INCLUDE_RAW_DATA = False     


PERSIST_STORAGE = False            
STORAGE_OUTPUT_DIR = "output/"


WHOIS_TIMEOUT = 10
SOCIAL_MEDIA_PLATFORMS = ["twitter", "linkedin", "github"]