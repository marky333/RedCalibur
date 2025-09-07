from transformers import pipeline

def summarize_recon_data(raw_data):
    """
    Summarize reconnaissance data into human-readable insights.

    Args:
        raw_data (str): The raw reconnaissance data.

    Returns:
        str: A summarized version of the data.
    """
    try:
        summarizer = pipeline("summarization")
        summary = summarizer(raw_data, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error in summarization: {str(e)}"
