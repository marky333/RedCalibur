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
        print(f"Results found: {results['total']}")
        for result in results['matches']:
            print(f"IP: {result['ip_str']}")
            print(result['data'])
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
        print(f"IP: {host['ip_str']}")
        print(f"Organization: {host.get('org', 'n/a')}")
        print(f"Operating System: {host.get('os', 'n/a')}")

        for item in host['data']:
            print(f"Port: {item['port']}")
            print(f"Banner: {item['data']}")
        return host

    except shodan.APIError as e:
        print(f"Error: {e}")
        return None