from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
import requests

DEFAULT_DIRS = ["admin","login","dashboard","uploads","api","docs",".git/","server-status"]

class DirEnumerator:
    def __init__(self, base_url: str, wordlist: str | None, threads: int = 10, timeout: float = 8.0):
        self.base = base_url.rstrip("/") + "/"
        self.wordlist = wordlist
        self.threads = threads
        self.timeout = timeout

    def _load_words(self):
        if self.wordlist:
            try:
                with open(self.wordlist, "r", encoding="utf-8", errors="ignore") as f:
                    return [w.strip().lstrip('/') for w in f if w.strip()]
            except Exception:
                pass
        return DEFAULT_DIRS

    def _probe(self, path: str):
        url = urljoin(self.base, path)
        try:
            r = requests.get(url, timeout=self.timeout, allow_redirects=False)
            if r.status_code in (200, 301, 302, 403):
                return f"{url} [{r.status_code}]"
        except Exception:
            pass
        return None

    def run(self):
        words = self._load_words()
        found = []
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futs = [ex.submit(self._probe, w) for w in words]
            for fu in as_completed(futs):
                res = fu.result()
                if res:
                    found.append(res)
        return sorted(found)
