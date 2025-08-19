import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

PAYLOADS = ['"<script>alert(1)</script>', "'><svg onload=alert(1)>"]

class XSSScanner:
    def __init__(self, url: str, timeout: float = 8.0):
        self.url = url
        self.timeout = timeout

    def _inject(self, url: str, payload: str):
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if not qs:
            return None
        new_qs = {k: payload for k in qs}
        new_url = urlunparse(parsed._replace(query=urlencode(new_qs)))
        try:
            r = requests.get(new_url, timeout=self.timeout)
            if payload.strip('"') in r.text or payload in r.text:
                return {"url": new_url, "payload": payload, "reflected": True}
        except Exception:
            pass
        return None

    def run(self):
        findings = []
        for pl in PAYLOADS:
            res = self._inject(self.url, pl)
            if res:
                findings.append(res)
        # basic form check
        try:
            r = requests.get(self.url, timeout=self.timeout)
            soup = BeautifulSoup(r.text, "html.parser")
            inputs = [i.get("name") for i in soup.find_all("input") if i.get("name")]
            if inputs:
                findings.append({"forms_inputs": inputs})
        except Exception:
            pass
        return findings
