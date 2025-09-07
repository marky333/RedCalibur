import requests

def get_http_headers(url):
    """
    Retrieve HTTP headers for the given URL.

    Args:
        url (str): The URL to analyze.

    Returns:
        dict: A dictionary containing HTTP headers.
    """
    try:
        response = requests.head(url)
        return response.headers
    except Exception as e:
        return {"error": str(e)}
