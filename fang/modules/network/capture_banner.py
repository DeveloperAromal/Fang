import socket
from urllib.parse import urlparse
import ssl


class CaptureBanner:

    def __init__(self, host: str, port: int):
        self.host = self._sanitize_host(host)
        self.port = port

    def _sanitize_host(self, host: str) -> str:
        parsed = urlparse(host)
        return parsed.hostname if parsed.hostname else host.rstrip("/")

    def grab(self) -> dict:
        try:
            with socket.create_connection((self.host, self.port), timeout=5) as sock:
                sock.settimeout(5)

                # Use SSL wrap for HTTPS ports
                if self.port == 443:
                    try:
                        ctx = ssl.create_default_context()
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
                "error": str(e)
            }

    def _detect_service(self, banner: bytes) -> dict:
        text = banner.decode(errors="ignore").lower()

        if b"mysql_native_password" in banner or self.port == 3306:
            return self._parse_mysql(banner)

        if text.startswith("220") and "ftp" in text:
            return {
                "service": "ftp",
                "banner": text.strip()
            }

        if text.startswith("ssh-"):
            return {
                "service": "ssh",
                "banner": text.strip()
            }

        if "http" in text:
            return {
                "service": "http",
                "banner": text.strip()
            }

        return {
            "service": "unknown"
        }

    def _parse_mysql(self, banner: bytes) -> dict:
        try:
            version = banner[5:].split(b'\x00')[0].decode()
            auth_plugin = banner.split(b'\x00')[-2].decode(errors="ignore")

            return {
                "service": "mysql",
                "mysql_version": version,
                "auth_plugin": auth_plugin
            }

        except Exception:
            return {"service": "mysql", "parse_error": True}