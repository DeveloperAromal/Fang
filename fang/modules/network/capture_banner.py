"""
Service banner grabbing for open TCP ports.

Connects directly to a host:port, sends a minimal protocol-appropriate
probe (HTTP GET for web ports, nothing for others), and reads back
whatever the service sends. Used by the recon pipeline to fingerprint
service versions after a port scan has identified open ports.

Performs live network connections. Only run against hosts you are
authorized to test.
"""

import socket
import ssl
from urllib.parse import urlparse


class CaptureBanner:
    
    """
    Grabs and lightly parses the banner returned by a single open port.

    Attributes:
        host: Sanitized hostname (scheme/path stripped if a URL was given).
        port: TCP port to connect to.
    """

    def __init__(self, host: str, port: int):
        self.host = self._sanitize_host(host)
        self.port = port

    def _sanitize_host(self, host: str) -> str:
        
        """
        Strip scheme/path from a URL-like input, leaving just the hostname.

        Accepts either a bare hostname ("example.com") or a full URL
        ("https://example.com/path") so callers don't need to normalize
        input before constructing this class.

        Args:
            host: Hostname or URL.

        Returns:
            Bare hostname, with any trailing slash removed if no scheme
            was present.
        """
        
        parsed = urlparse(host)
        return parsed.hostname if parsed.hostname else host.rstrip("/")

    def grab(self) -> dict:
        
        """
        Connect to host:port and capture whatever banner is returned.

        Behavior depends on the port:
            - 443: wraps the connection in TLS (certificate validation
              disabled we only want the banner, not a trusted handshake)
              and sends a bare HTTP GET.
            - 80, 8080: sends a bare HTTP GET over plain TCP.
            - any other port: no probe is sent; we just read whatever the
              service sends unprompted (common for SSH, FTP, SMTP, etc).

        All socket and protocol errors during the probe are swallowed so a
        single unresponsive service doesn't interrupt a larger scan; in
        that case `banner` is left empty rather than raising.

        Returns:
            On success, a dict with:
                host, port, raw_banner (bytes), decoded_banner (str),
                and service-specific keys from `_detect_service`
                (e.g. "service", "banner", or "mysql_version").
                
            On connection failure (e.g. timeout, refused), a dict with:
                host, port, error (str) note this dict will NOT contain
                raw_banner/decoded_banner/service, so callers should check
                for the "error" key before reading those fields.
        """
        
        try:
            with socket.create_connection((self.host, self.port), timeout=5) as sock:
                sock.settimeout(5)

                if self.port == 443:
                    try:
                        ctx = ssl.create_default_context()
                        # Cert validation is intentionally disabled: we're
                        # grabbing a banner for recon, not establishing a
                        # trusted connection, and many targets use
                        # self-signed or expired certs.
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        with ctx.wrap_socket(sock, server_hostname=self.host) as ssock:
                            try:
                                ssock.sendall(b"GET / HTTP/1.0\r\nHost: %b\r\n\r\n" % self.host.encode())
                            except Exception:
                                pass
                            banner = ssock.recv(4096)
                    except Exception:
                        pass

                elif self.port in (80, 8080):
                    try:
                        req = f"GET / HTTP/1.0\r\nHost: {self.host}\r\n\r\n".encode()
                        sock.sendall(req)
                    except Exception:
                        pass

                    try:
                        banner = sock.recv(4096)
                    except socket.timeout:
                        banner = b""

                else:
                    # Non-HTTP(S) ports: stay silent and just read whatever
                    # the service announces on connect (e.g. SSH/FTP banners).
                    try:
                        banner = sock.recv(2048)
                    except socket.timeout:
                        banner = b""

            result = {
                "host": self.host,
                "port": self.port,
                "raw_banner": banner,
                "decoded_banner": banner.decode(errors="ignore") if banner else "",
            }

            service_info = self._detect_service(banner)
            result.update(service_info)

            return result

        except Exception as e:
            return {
                "host": self.host,
                "port": self.port,
                "error": str(e),
            }

    def _detect_service(self, banner: bytes) -> dict:
        
        """
        Guess the service type from banner content using simple heuristics.

        Checks, in order: MySQL handshake markers, FTP greeting ("220 ...
        ftp"), SSH version string ("SSH-..."), then a generic "http"
        keyword match. This is intentionally crude it's a fast first
        pass, not a definitive fingerprint.

        Args:
            banner: Raw bytes read from the socket.

        Returns:
            A dict with at least a "service" key (one of "mysql", "ftp",
            "ssh", "http", or "unknown"), plus a "banner" key with the
            cleaned text for the matched cases.
        """
        
        text = banner.decode(errors="ignore").lower()

        if b"mysql_native_password" in banner or self.port == 3306:
            return self._parse_mysql(banner)

        if text.startswith("220") and "ftp" in text:
            return {
                "service": "ftp",
                "banner": text.strip(),
            }

        if text.startswith("ssh-"):
            return {
                "service": "ssh",
                "banner": text.strip(),
            }

        if "http" in text:
            return {
                "service": "http",
                "banner": text.strip(),
            }

        return {
            "service": "unknown",
        }

    def _parse_mysql(self, banner: bytes) -> dict:
        
        """
        Extract version and auth plugin from a MySQL handshake packet.

        MySQL's initial handshake packet has a fixed layout: a null-byte
        separates the protocol version, server version string, and
        connection ID. We grab the version (bytes 5 onward, up to the
        first null) and assume the auth plugin name is the second-to-last
        null-delimited field this works for standard handshakes but is
        not a full protocol parse.

        Args:
            banner: Raw bytes from the MySQL handshake.

        Returns:
            {"service": "mysql", "mysql_version": str, "auth_plugin": str}
            on success, or {"service": "mysql", "parse_error": True} if the
            banner doesn't match the expected layout.
        """
        
        try:
            version = banner[5:].split(b'\x00')[0].decode()
            auth_plugin = banner.split(b'\x00')[-2].decode(errors="ignore")

            return {
                "service": "mysql",
                "mysql_version": version,
                "auth_plugin": auth_plugin,
            }

        except Exception:
            return {"service": "mysql", "parse_error": True}