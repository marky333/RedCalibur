import ssl
import socket
from datetime import datetime

def get_ssl_details(hostname):
    """
    Retrieve SSL/TLS certificate details for the given hostname.

    Args:
        hostname (str): The hostname to analyze.

    Returns:
        dict: A dictionary containing SSL/TLS certificate details.
    """
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return {
                    "issuer": dict(x[0] for x in cert["issuer"]),
                    "subject": dict(x[0] for x in cert["subject"]),
                    "version": cert.get("version"),
                    "serialNumber": cert.get("serialNumber"),
                    "notBefore": datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z"),
                    "notAfter": datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z"),
                    "subjectAltName": cert.get("subjectAltName", [])
                }
    except Exception as e:
        return {"error": str(e)}
