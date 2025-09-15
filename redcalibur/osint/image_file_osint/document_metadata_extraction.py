from PyPDF2 import PdfReader

def extract_document_metadata(file_path):
    """
    Extract metadata from a document (e.g., PDF).

    Args:
        file_path (str): The path to the document file.

    Returns:
        dict: A dictionary containing document metadata.
    """
    try:
        reader = PdfReader(file_path)
        metadata = reader.metadata

        if not metadata:
            return {"error": "No metadata found."}

        return {key: metadata[key] for key in metadata}
    except Exception as e:
        return {"error": str(e)}
