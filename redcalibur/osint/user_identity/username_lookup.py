import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
import requests

# Initialize logger
logger = logging.getLogger("username_lookup")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
)

# Simple platform URL patterns; can be extended
PLATFORM_URLS: Dict[str, str] = {
    "twitter": "https://twitter.com/{username}",
    "instagram": "https://www.instagram.com/{username}/",
    "github": "https://github.com/{username}",
    "linkedin": "https://www.linkedin.com/in/{username}/",
    "reddit": "https://www.reddit.com/user/{username}/",
    "medium": "https://medium.com/@{username}",
}

def _probe_profile(url: str, timeout: float = 3.0) -> bool:
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout, allow_redirects=True)
        # Basic heuristic: 200 => exists; certain platforms (LinkedIn) may return 999/other codes for blocked
        if resp.status_code == 200:
            return True
        # Handle GitHub not found page (404)
        if resp.status_code == 404:
            return False
        # Treat other codes as not found/blocked without failing
        return False
    except requests.RequestException as e:
        logger.debug(f"Probe error for {url}: {e}")
        return False

def lookup_username(username: str, platforms: List[str]) -> Dict[str, str]:
    """
    Lookup a username across multiple platforms via HTTP probes (no external CLI).

    Args:
        username: Username to check
        platforms: List of platform keys, e.g., ["twitter","github"]

    Returns:
        dict mapping platform -> profile URL if found; otherwise 'not found'.
    """
    results: Dict[str, str] = {}

    tasks = {}
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(platforms)))) as ex:
        for p in platforms:
            template = PLATFORM_URLS.get(p.lower())
            if not template:
                results[p] = "unsupported platform"
                continue
            url = template.format(username=username)
            tasks[ex.submit(_probe_profile, url)] = (p, url)

        for fut in as_completed(tasks):
            p, url = tasks[fut]
            try:
                exists = fut.result()
                results[p] = url if exists else "not found"
            except Exception as e:
                results[p] = f"error: {e}"

    return results
