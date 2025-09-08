import google.generativeai as genai
import os

def summarize_recon_data(raw_data: str) -> str:
    """
    Summarizes reconnaissance data into a human-readable report for a non-technical audience.

    Args:
        raw_data (str): The raw reconnaissance data in JSON format.

    Returns:
        str: A summarized, easy-to-understand report.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Error: GEMINI_API_KEY not found. Please set it in your environment."

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        You are an expert cybersecurity analyst tasked with explaining technical findings to a non-technical audience.
        Based on the following OSINT data, create a clear, concise, and easy-to-understand summary.
        Focus on the key risks and actionable recommendations. Avoid jargon.

        **Raw Data:**
        {raw_data}

        **Summary for a Non-Technical Audience:**
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"An error occurred during summarization with Gemini API: {str(e)}"
