import requests
from bs4 import BeautifulSoup

def perform_google_dorking(query, num_results=10):
    """
    Perform Google Dorking for the given query.

    Args:
        query (str): The Google Dorking query.
        num_results (int): Number of results to fetch.

    Returns:
        list: A list of URLs matching the query.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        url = f"https://www.google.com/search?q={query}&num={num_results}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and "http" in href:
                results.append(href)

        return results[:num_results]
    except Exception as e:
        return {"error": str(e)}
