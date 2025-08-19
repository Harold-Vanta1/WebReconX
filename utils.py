from urllib.parse import urlparse, urlunparse, urlencode, parse_qs
import requests

def normalize_base(url: str) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme or "http"
    netloc = parsed.netloc or parsed.path
    return f"{scheme}://{netloc}".rstrip("/")

def get(path: str, timeout: float = 8.0, headers: dict | None = None):
    return requests.get(path, timeout=timeout, headers=headers or default_headers())

def default_headers():
    return {
        "User-Agent": "WebReconX/0.1 (+https://github.com)",
        "Accept": "*/*",
    }

def set_query(url: str, params: dict) -> str:
    parsed = urlparse(url)
    q = parse_qs(parsed.query)
    for k,v in params.items():
        q[k] = [v]
    new_q = urlencode({k:v[0] for k,v in q.items()})
    return urlunparse(parsed._replace(query=new_q))
