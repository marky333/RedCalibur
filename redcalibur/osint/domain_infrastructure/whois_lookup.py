import socket
import whois

def perform_whois_lookup(domain):
    """
    Perform a WHOIS lookup for the given domain.

    Args:
        domain (str): The domain name to look up.

    Returns:
        dict: A dictionary containing WHOIS information.
    """
    try:
        whois_info = whois.whois(domain)
        if isinstance(whois_info, dict):
            return whois_info
        return whois_info.__dict__
    except Exception as e:
        return {"error": str(e)}

def is_valid_domain(domain):
    """
    Validate the domain name.

    Args:
        domain (str): The domain name to validate.

    Returns:
        bool: True if the domain is valid, False otherwise.
    """
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False
