LLM_PROVIDER = ""         
LLM_API_KEY = ""              
LLM_MODEL = ""   
LLM_MAX_TOKENS = 4096

TOOLS_AVAILABLE = [
    {
        "name": "scan_ports",
        "description": "Scan open ports of a target. Returns open ports, protocols, and service info."
    },
    {
        "name": "grab_banners",
        "description": "Grab banners from open ports to identify running services and versions. Requires port scan to run first."
    },
    {
        "name": "parse_robots",
        "description": "Parse robots.txt of a target. Reveals disallowed paths and hidden endpoints."
    },
    {
        "name": "enumerate_subdomains",
        "description": "Enumerate subdomains of a target using a wordlist. Expands the attack surface."
    },
    {
        "name": "fingerprint_tech",
        "description": "Fingerprint web technologies used by the target (CMS, frameworks, servers, JS libraries)."
    },
    {
        "name": "crawl_urls",
        "description": "Crawl URLs from the target website. Maps endpoints and discovers hidden pages."
    },
    {
        "name": "scrape_web",
        "description": "Scrape raw HTML content from the target. Useful for finding comments, metadata, and exposed data."
    },
    {
        "name": "domain_details",
        "description": "Get OSINT domain details including WHOIS, registrar, DNS records, and IP info."
    },
    {
        "name": "social_media_osint",
        "description": "Extract social media presence and data linked to the target domain or organization."
    },
]


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


REPORT_OUTPUT_DIR = "reports/"
REPORT_FORMAT = "markdown"         
REPORT_INCLUDE_RAW_DATA = False     


PERSIST_STORAGE = False            
STORAGE_OUTPUT_DIR = "output/"


WHOIS_TIMEOUT = 10
SOCIAL_MEDIA_PLATFORMS = ["twitter", "linkedin", "github"]