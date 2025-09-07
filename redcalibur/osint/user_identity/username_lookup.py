import requests

def lookup_username(username, platforms):
    """
    Lookup a username across multiple platforms.

    Args:
        username (str): The username to search for.
        platforms (list): A list of platforms to search on.

    Returns:
        dict: A dictionary with platform names as keys and URLs as values.
    """
    results = {}

    for platform in platforms:
        url = f"https://{platform}.com/{username}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results[platform] = url
            else:
                results[platform] = "Not Found"
        except Exception as e:
            results[platform] = str(e)

    return results
