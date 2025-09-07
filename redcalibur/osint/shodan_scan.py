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
        # Initialize Shodan client
        api = shodan.Shodan(api_key)

        # Perform Shodan scan
        result = api.host(target)
        return result
    except shodan.APIError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    api_key = input("Enter your Shodan API key: ")
    target = input("Enter the target IP or domain for Shodan scan: ")

    if api_key and target:
        result = perform_shodan_scan(api_key, target)
        print("Shodan Scan Result:")
        print(result)
    else:
        print("API key and target are required.")
