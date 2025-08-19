import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, quote

PARAMS = ["next","url","redirect","dest","destination","redir"]

class OpenRedirectScanner:
    def __init__(self, url: str, timeout: float = 8.0):
        self.url = url
        self.timeout = timeout

    def run(self):
        parsed = urlparse(self.url)
        qs = parse_qs(parsed.query)
        if not qs:
            return []
        findings = []
        for p in PARAMS:
            if p in qs:
                evil = "https://example.com"
                new_qs = {**{k:v[0] for k,v in qs.items()}, p: evil}
                new_url = urlunparse(parsed._replace(query=urlencode(new_qs)))
                try:
                    r = requests.get(new_url, timeout=self.timeout, allow_redirects=False)
                    if r.status_code in (301,302) and r.headers.get("Location","").startswith("https://example.com"):
                        findings.append({"param": p, "url": new_url, "open_redirect": True})
                except Exception:
                    pass
        return findings
