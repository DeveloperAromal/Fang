from typing import Dict, Any
from langchain.tools import tool

from fang.modules.network.port_scanner import PortScanner
from fang.modules.web.basic.robots_parser import RobotsParser
from fang.modules.web.basic.subdomain_enumerator import SubdomainEnumerator
from fang.modules.web.basic.tech_fingerprint import TechFingerprint
from fang.modules.web.basic.url_crawler import URLCrawler
from fang.modules.web.basic.web_scrapper import WebScraper
from fang.modules.web.osint.domain_details import DomainDetails
from fang.modules.web.osint.social_media_data_extracter import SocialMediaDataOSINT


@tool
def scan_port(target: str) -> Dict[str, Any]:
    """Scan open ports of a target."""
    return PortScanner(target).scan()


@tool
def robots(target: str) -> Dict[str, Any]:
    """Parse robots.txt of a target."""
    return RobotsParser(target).parse()


@tool
def subdomain_enum(target: str) -> Dict[str, Any]:
    """Enumerate subdomains."""
    return SubdomainEnumerator(target).scan()


@tool
def tech_fingerprint(target: str) -> Dict[str, Any]:
    """Fingerprint web technologies."""
    return TechFingerprint(target).fingerprint()


@tool
def crawl_urls(target: str) -> Dict[str, Any]:
    """Crawl URLs from target."""
    return URLCrawler(target).crawl()


@tool
def web_scrape(target: str) -> Dict[str, Any]:
    """Scrape web page content."""
    return WebScraper(target).scrape()


@tool
def domain_details(target: str) -> Dict[str, Any]:
    """Get domain OSINT details."""
    return DomainDetails(target).scan()


@tool
def social_media_osint(target: str) -> Dict[str, Any]:
    """Extract social media data from target."""
    return SocialMediaDataOSINT(target).osint()