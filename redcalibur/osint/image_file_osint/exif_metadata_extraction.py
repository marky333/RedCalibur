from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif_metadata(image_path):
    """
    Extract EXIF metadata from an image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        dict: A dictionary containing EXIF metadata.
    """
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return {"error": "No EXIF metadata found."}

        metadata = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            metadata[tag_name] = value

        return metadata
    except Exception as e:
        return {"error": str(e)}
