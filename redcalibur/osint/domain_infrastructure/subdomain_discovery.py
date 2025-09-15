import requests

def discover_subdomains(domain, subdomain_list):
    """
    Discover subdomains for the given domain using a wordlist.

    Args:
        domain (str): The domain name to search.
        subdomain_list (list): A list of potential subdomains.

    Returns:
        list: A list of discovered subdomains.
    """
    discovered_subdomains = []

    for subdomain in subdomain_list:
        url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                discovered_subdomains.append(url)
        except requests.ConnectionError:
            pass

    return discovered_subdomains
