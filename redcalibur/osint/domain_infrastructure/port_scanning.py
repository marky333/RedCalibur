import socket

def perform_port_scan(target, ports):
    """
    Perform a port scan on the target.

    Args:
        target (str): The target IP or domain.
        ports (list): A list of ports to scan.

    Returns:
        dict: A dictionary with port statuses.
    """
    port_status = {}

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.6)
            try:
                result = s.connect_ex((target, port))
                port_status[port] = "Open" if result == 0 else "Closed"
            except Exception as e:
                port_status[port] = f"Error: {e}"

    return port_status
