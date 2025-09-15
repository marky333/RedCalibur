import requests

def scan_url(api_key: str, url: str):
    """
    Scan a URL using the VirusTotal API.

    :param api_key: Your VirusTotal API key
    :param url: The URL to scan
    :return: Scan results
    """
    vt_url = "https://www.virustotal.com/api/v3/urls"
    headers = {
        "x-apikey": api_key
    }
    data = {
        "url": url
    }

    response = requests.post(vt_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_url_report(api_key: str, url_id: str):
    """
    Get the scan report for a URL using the VirusTotal API.

    :param api_key: Your VirusTotal API key
    :param url_id: The ID of the scanned URL
    :return: Report results
    """
    vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {
        "x-apikey": api_key
    }

    response = requests.get(vt_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
