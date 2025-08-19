from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import socket

DEFAULT_WORDS = ["www","mail","dev","test","staging","api","admin","beta"]

class SubdomainEnumerator:
    def __init__(self, base_url: str, wordlist: str | None, threads: int = 10):
        self.base_url = base_url
        self.wordlist = wordlist
        self.threads = threads

    def _load_words(self):
        if self.wordlist:
            try:
                with open(self.wordlist, "r", encoding="utf-8", errors="ignore") as f:
                    return [w.strip() for w in f if w.strip()]
            except Exception:
                pass
        return DEFAULT_WORDS

    def _resolve(self, host: str):
        try:
            socket.gethostbyname(host)
            return host
        except Exception:
            return None

    def run(self):
        domain = urlparse(self.base_url).netloc or self.base_url
        words = self._load_words()
        found = []
        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futs = [ex.submit(self._resolve, f"{w}.{domain}") for w in words]
            for fu in as_completed(futs):
                res = fu.result()
                if res:
                    found.append(f"https://{res}")
        return sorted(found)
