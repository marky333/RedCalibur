import requests
from urllib.parse import urlparse

DEFAULT_TIMEOUT = 6.0


def normalize_url(url: str) -> str:
    if not url.lower().startswith(("http://", "https://")):
        return "http://" + url
    return url


def basic_url_health(url: str) -> dict:
    """
    Lightweight URL health check used when VirusTotal is unavailable.
    Returns status code, final URL, and a small set of headers.
    """
    out = {"input": url}
    try:
        url = normalize_url(url)
        resp = requests.get(url, timeout=DEFAULT_TIMEOUT, allow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127 Safari/537.36"
        })
        out.update({
            "status": resp.status_code,
            "final_url": resp.url,
            "headers": {k: v for k, v in resp.headers.items() if k.lower() in {"server", "content-type", "x-frame-options", "strict-transport-security"}},
        })
    except requests.RequestException as e:
        out["error"] = str(e)
    return out
