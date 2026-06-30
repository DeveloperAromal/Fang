"""
TCP port scanning.

Resolves a target URL/hostname to an IP, then attempts a TCP connect
to every port listed in data/ports.json, in parallel via a thread
pool. Reports which ports are open and maps each to a known service
name from that same lookup file.

Performs live network connections. Only run against hosts you are
authorized to test.
"""

import json
import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse


class PortScanner():
    
    """
    Scans a host for open TCP ports using a configurable port/service list.

    The set of ports scanned is driven entirely by data/ports.json
    (mapping port number -> service name), not hardcoded, so adding or
    removing ports to scan only requires editing that file.

    Attributes:
        url: Original target string as passed in (URL or bare host).
        open_ports: Currently unused placeholder; results are built and
            returned fresh from `scan()` rather than accumulated here.
        service_map: Dict of {"port_str": "service_name"} loaded from
            data/ports.json.
        ports: List of int port numbers derived from service_map's keys.
    """

    def __init__(self, url: str):
        self.url = url

        self.open_ports = []
        self.service_map = self._load_ports()
        self.ports = list(map(int, self.service_map.keys()))

    def _get_host(self):
        
        """
        Extract a bare hostname from self.url.

        Handles both full URLs ("https://example.com/path") and bare
        hosts ("example.com") since urlparse only populates `netloc`
        for the former.

        Returns:
            Hostname string suitable for DNS resolution.
        """
        parsed = urlparse(self.url)

        return parsed.netloc if parsed.netloc else parsed.path

    def _resolve_ip(self, host):
        
        """
        Resolve a hostname to an IPv4 address.

        Args:
            host: Hostname to resolve.

        Returns:
            IPv4 address as a string.

        Raises:
            socket.gaierror: If the hostname cannot be resolved. Not
                caught here, so callers (currently `scan()`) should
                expect `scan()` to raise on an unresolvable target
                rather than returning an error dict.
        """
        
        return socket.gethostbyname(host)

    def _load_ports(self):
        
        """
        Load the port -> service name lookup table from disk.

        Resolves the path relative to this file's location
        (../../data/ports.json from fang/modules/network/), so it
        works regardless of the working directory the scanner is
        invoked from.

        Returns:
            Dict of {"port_str": "service_name"}.
        """
        
        BASE_DIR = Path(__file__).resolve().parents[2]
        DIR_PATH = BASE_DIR / "data" / "ports.json"

        with open(DIR_PATH, "r") as f:
            return json.load(f)

    def _find_service(self, port: int):
        
        """
        Look up the known service name for a port.

        Args:
            port: Port number.

        Returns:
            Service name string, or "unknown" if the port isn't in
            service_map.
        """
        
        return self.service_map.get(str(port), "unknown")

    def _scan_port(self, ip, port):
        
        """
        Attempt a TCP connect to a single port.

        Uses connect_ex (rather than connect) so a closed/filtered port
        returns a nonzero error code instead of raising, keeping this
        cheap to call across many ports/threads. A 1-second timeout
        keeps closed/filtered ports from stalling the scan.

        Any exception (e.g. network errors) is silently swallowed and
        treated the same as a closed port this method does not
        distinguish "closed" from "errored."

        Args:
            ip: Target IP address.
            port: Port number to test.

        Returns:
            The port number if open (connect_ex returned 0), otherwise
            None.
        """
        
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
        
        """
        Run the full port scan against self.url and return a summary.

        Resolves the host to an IP once, then fans out `_scan_port`
        across all configured ports using up to 50 worker threads.
        Open ports are enriched with their known service name before
        being returned.

        Returns:
            {
                "host": str,            # resolved hostname
                "ip": str,              # resolved IP address
                "total_scanned": int,   # number of ports attempted
                "open_ports_count": int,
                "open_ports": [
                                    {
                                        "port": int,
                                        "service": str
                                    }, 
                                    ...
                                ]
            }

        Raises:
            socket.gaierror: If the host in self.url cannot be resolved.
        """
        
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