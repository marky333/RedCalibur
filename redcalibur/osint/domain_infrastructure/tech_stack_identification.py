import requests
from bs4 import BeautifulSoup

def identify_tech_stack(url):
    """
    Identify the tech stack used by the given URL.

    Args:
        url (str): The URL to analyze.

    Returns:
        dict: A dictionary containing identified technologies.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Check for common technologies in meta tags or scripts
        tech_stack = {
            "frameworks": [],
            "libraries": []
        }

        if "React" in response.text:
            tech_stack["frameworks"].append("React")
        if "Angular" in response.text:
            tech_stack["frameworks"].append("Angular")
        if "jQuery" in response.text:
            tech_stack["libraries"].append("jQuery")

        return tech_stack
    except Exception as e:
        return {"error": str(e)}
