import re

class MemoryFilter:
    
    def __call__(self, raw: dict) -> dict:
        return {
            "port_scan": self._filter_port_scan(raw.get("port_scan", {})),
            "services": [self._filter_banner(b) for b in raw.get("banners", []) if self._has_useful_data(b)]
        }


    def _filter_port_scan(self, scan: dict) -> dict:
        return {
            "host": scan.get("host"),
            "ip": scan.get("ip"),
            "total_scanned": scan.get("total_scanned"),
            "open_ports": scan.get("open_ports", [])
        }


    def _filter_banner(self, banner: dict) -> dict:
        port = banner.get("port")
        service = banner.get("service", "unknown")
        decoded = banner.get("decoded_banner", "")
        out = {
                "port": port, 
                "service": service
            }

        if port == 21:
            sw = re.search(r"Welcome to (\S+)", decoded)
            out["software"] = sw.group(1) if sw else "unknown"
            out["tls"] = "[TLS]" in decoded
            out["anonymous_login"] = "No anonymous login" not in decoded


        elif service == "http":
            status = re.search(r"HTTP/[\d.]+ (\d+ \w+)", decoded)
            location = re.search(r"location: (.+)\r\n", decoded, re.IGNORECASE)
            title = re.search(r"<title>(.+?)</title>", decoded, re.IGNORECASE | re.DOTALL)
            out["status"] = status.group(1) if status else None
            
            
            if location: out["redirects_to"] = location.group(1).strip()
            if title: out["page_title"] = title.group(1).strip()

        elif service == "mysql":
            out["version"] = banner.get("mysql_version")
            out["auth_plugin"] = banner.get("auth_plugin")

        elif port == 110:
            sw = re.search(r"\+OK (\w+)", decoded)
            out["software"] = sw.group(1) if sw else "unknown"

        return out


    def _has_useful_data(self, banner: dict) -> bool:
        return bool(banner.get("decoded_banner") or banner.get("mysql_version"))