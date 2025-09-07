import requests

def detect_cdn_and_hosting(url):
    """
    Detect the CDN and hosting provider for the given URL.

    Args:
        url (str): The URL to analyze.

    Returns:
        dict: A dictionary containing CDN and hosting provider information.
    """
    try:
        response = requests.get(url)
        headers = response.headers

        cdn_hosting_info = {
            "cdn": None,
            "hosting_provider": None
        }

        # Example: Check for common CDN headers
        if "cloudflare" in headers.get("server", "").lower():
            cdn_hosting_info["cdn"] = "Cloudflare"
        if "akamai" in headers.get("server", "").lower():
            cdn_hosting_info["cdn"] = "Akamai"

        # Hosting provider detection (basic example)
        if "x-amz-id" in headers:
            cdn_hosting_info["hosting_provider"] = "Amazon AWS"

        return cdn_hosting_info
    except Exception as e:
        return {"error": str(e)}
