import phonenumbers
from phonenumbers import carrier, geocoder

def footprint_phone_number(phone_number):
    """
    Perform footprinting on a phone number.

    Args:
        phone_number (str): The phone number to analyze.

    Returns:
        dict: A dictionary containing carrier and location information.
    """
    try:
        parsed_number = phonenumbers.parse(phone_number)
        carrier_info = carrier.name_for_number(parsed_number, "en")
        location_info = geocoder.description_for_number(parsed_number, "en")

        return {
            "phone_number": phone_number,
            "carrier": carrier_info,
            "location": location_info
        }
    except Exception as e:
        return {"error": str(e)}
