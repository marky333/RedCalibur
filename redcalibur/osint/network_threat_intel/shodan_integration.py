import shodan

def perform_shodan_scan(api_key, target):
    """
    Perform a Shodan scan for the given target.

    Args:
        api_key (str): The Shodan API key.
        target (str): The target IP or domain to scan.

    Returns:
        dict: A dictionary containing Shodan scan results.
    """
    try:
        api = shodan.Shodan(api_key)
        result = api.host(target)
        return result
    except shodan.APIError as e:
        return {"error": str(e)}
