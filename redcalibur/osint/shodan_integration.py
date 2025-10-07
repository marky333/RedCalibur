import shodan

def search_shodan(api_key: str, query: str):
    """
    Search Shodan for a specific query.

    :param api_key: Your Shodan API key
    :param query: The search query
    :return: Search results
    """
    api = shodan.Shodan(api_key)

    try:
        results = api.search(query)
        total = results.get('total', 0) if isinstance(results, dict) else 0
        print(f"Results found: {total}")
        for result in results.get('matches', []) if isinstance(results, dict) else []:
            ip = result.get('ip_str', 'unknown')
            print(f"IP: {ip}")
            banner = result.get('data')
            if banner:
                print(banner)
            print("")
        return results

    except shodan.APIError as e:
        print(f"Error: {e}")
        return None

def get_host_info(api_key: str, ip: str):
    """
    Get detailed information about a specific host.

    :param api_key: Your Shodan API key
    :param ip: The IP address of the host
    :return: Host information
    """
    api = shodan.Shodan(api_key)

    try:
        host = api.host(ip)
        print(f"IP: {host.get('ip_str', ip)}")
        print(f"Organization: {host.get('org', 'n/a')}")
        print(f"Operating System: {host.get('os', 'n/a')}")

        for item in host.get('data', []) if isinstance(host, dict) else []:
            print(f"Port: {item.get('port', 'n/a')}")
            print(f"Banner: {item.get('data', '')}")
        return host

    except shodan.APIError as e:
        print(f"Error: {e}")
        return None