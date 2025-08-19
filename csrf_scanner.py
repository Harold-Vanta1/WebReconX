import requests
from bs4 import BeautifulSoup

class CSRFScanner:
    def __init__(self, url: str, timeout: float = 8.0):
        self.url = url
        self.timeout = timeout

    def run(self):
        findings = []
        try:
            r = requests.get(self.url, timeout=self.timeout)
            soup = BeautifulSoup(r.text, "html.parser")
            for form in soup.find_all("form"):
                method = (form.get("method") or "get").lower()
                inputs = [i.get("name","") for i in form.find_all("input")]
                has_token = any("csrf" in (name or "").lower() for name in inputs)
                if method == "post" and not has_token:
                    findings.append({"form_action": form.get("action",""), "issue": "No CSRF token field detected"})
        except Exception:
            pass
        return findings
