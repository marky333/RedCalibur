import requests
from bs4 import BeautifulSoup

def scrape_social_media(platform, username):
    """
    Scrape social media profile information for the given username.

    Args:
        platform (str): The social media platform (e.g., 'twitter', 'instagram').
        username (str): The username to scrape.

    Returns:
        dict: A dictionary containing profile information.
    """
    try:
        url = f"https://{platform}.com/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract profile information (this is platform-specific and may require adjustments)
            profile_info = {
                "url": url,
                "status": "Profile found",
                "content": soup.prettify()[:500]  # Return the first 500 characters of the HTML
            }
            return profile_info
        else:
            return {"error": f"Profile not found (status code: {response.status_code})"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    platform = input("Enter the social media platform (e.g., 'twitter', 'instagram'): ")
    username = input("Enter the username to scrape: ")

    if platform and username:
        result = scrape_social_media(platform, username)
        print("Social Media Scraper Result:")
        print(result)
    else:
        print("Platform and username are required.")
