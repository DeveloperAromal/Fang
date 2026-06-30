"""
robots.txt fetching and parsing.

Checks whether a target host serves a robots.txt, then does a naive
line-by-line parse of it to pull out user-agents, allowed/disallowed
paths, and sitemap URLs. Used by the recon pipeline to surface paths
the site owner explicitly didn't want crawled, which are often the
most interesting ones.
"""

import requests
import urllib3
from requests.exceptions import SSLError

from fang.modules.web.basic.web_scrapper import WebScraper

# Suppress urllib3's warning about verify=False requests — we
# intentionally retry without TLS verification when a target's
# certificate is invalid, since recon shouldn't be blocked by that.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RobotsParser:
    
    """
    Fetches and parses robots.txt for a single target URL.

    Attributes:
        url: Target base URL with any trailing slash removed.
        has_robot: True if a robots.txt was found (status 200/201),
            determined once at construction time.
        scrapper: A WebScraper instance for the same URL. Currently
            unused within this class — kept for parity/future use.
        data: Parsed robots.txt contents, populated by `parse()`. See
            `parse()` for the shape.
    """

    def __init__(self, url: str):

        self.url = url.rstrip("/")
        self.has_robot = self._has_robot()
        self.scrapper = WebScraper(self.url)

        self.data = {
            "user-agents": [],
            "allowed": [],
            "disallowed": [],
            "sitemap": []
        }

    def _has_robot(self):
        """
        Check whether {url}/robots.txt exists and is reachable.

        Tries a normal HTTPS request first; if that fails due to an
        invalid/self-signed certificate, retries once with TLS
        verification disabled rather than giving up (recon targets
        often have broken certs). Any other request failure (timeout,
        connection refused, DNS failure, etc.) is treated as "no
        robots.txt".

        Returns:
            True if the request succeeded with status 200 or 201,
            False otherwise (including on any request failure).
        """
        
        url = f"{self.url}/robots.txt"
        try:
            res = requests.get(url, timeout=10)
        except SSLError:
            try:
                res = requests.get(url, timeout=10, verify=False)
            except Exception:
                return False
        except requests.RequestException:
            return False

        return res.status_code in (200, 201)

    def _extract_robots(self):
        """
        Fetch robots.txt again and populate self.data from its contents.

        No-op if `self.has_robot` is False. Re-fetches the file rather
        than reusing the response from `_has_robot()`, since that
        method only checks reachability and doesn't keep the body.

        Parsing is line-based and case-insensitive on directive names,
        matching any line containing "User-agent", "Allow", "Disallow",
        or "Sitemap" (in either case). This is a simple substring match,
        not a real robots.txt grammar parser, so it will also match
        these words if they appear in a comment or elsewhere in a line
        — except for "# Disallow" and "# Sitemaps" lines, which are
        explicitly skipped as comments.

        Values are stored with the directive prefix stripped (e.g.
        "Disallow: /admin" -> "/admin"), but are not otherwise trimmed
        of leading whitespace.

        Any request failure during the re-fetch is silently swallowed,
        leaving self.data at whatever was accumulated so far (possibly
        still all-empty lists).

        Side effects:
            Appends to self.data["user-agents"], ["allowed"],
            ["disallowed"], and ["sitemap"] in place.
        """
        
        if self.has_robot:

            url = f"{self.url}/robots.txt"

            try:
                try:
                    robots = requests.get(url, timeout=10).text
                except SSLError:
                    robots = requests.get(url, timeout=10, verify=False).text

                lines = robots.splitlines()

                for line in lines:

                    if "User-agent" in line or "user-agent" in line:

                        self.data["user-agents"].append(
                            line.replace("User-agent:", "").replace("user-agent:", "")
                        )

                    if "Allow" in line or "allow" in line:

                        self.data["allowed"].append(
                            line.replace("Allow:", "").replace("allow:", "")
                        )

                    if "Disallow" in line or "disallow" in line:

                        if "# Disallow" in line:

                            continue

                        self.data["disallowed"].append(
                            line.replace("Disallow:", "").replace("disallow:", "")
                        )

                    if "Sitemap" in line or "sitemap" in line:

                        if "# Sitemaps" in line:

                            continue

                        self.data["sitemap"].append(
                            line.replace("Sitemap:", "").replace("sitemap:", "")
                        )

            except requests.RequestException as e:

                pass

    def parse(self):
        """
        Run the parse and return the robots.txt data.

        Returns:
            {
                "user-agents": list[str],
                "allowed": list[str],
                "disallowed": list[str],
                "sitemap": list[str]
            }
            All lists are empty if no robots.txt was found or it had
            no matching directives.
        """
        
        self._extract_robots()

        return self.data