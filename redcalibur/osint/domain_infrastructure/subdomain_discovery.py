import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def discover_subdomains(domain, subdomain_list, timeout: float = 2.0, workers: int = 8):
    """
    Discover subdomains for the given domain using a wordlist.

    Args:
        domain (str): The domain name to search.
        subdomain_list (list): A list of potential subdomains.
        timeout (float): Per-request timeout seconds.
        workers (int): Number of parallel workers.

    Returns:
        list: A list of discovered subdomains (URLs).
    """
    discovered_subdomains = []

    def probe(sub: str):
        url = f"http://{sub}.{domain}"
        try:
            # HEAD is lighter; some hosts may not support it, so fallback to GET
            resp = requests.head(url, timeout=timeout, allow_redirects=True)
            if resp.status_code < 400:
                return url
            # Fallback to GET if HEAD inconclusive
            resp = requests.get(url, timeout=timeout, allow_redirects=True)
            if resp.status_code < 400:
                return url
        except requests.RequestException:
            return None
        return None

    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        futures = {ex.submit(probe, sub): sub for sub in subdomain_list}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res:
                    discovered_subdomains.append(res)
            except Exception:
                # ignore individual probe failures
                pass

    return discovered_subdomains
