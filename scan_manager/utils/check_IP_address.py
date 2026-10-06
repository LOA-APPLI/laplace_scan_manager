import re
import ipaddress
import socket


_PATTERN = re.compile(
    r"^(?:(?P<scheme>[a-zA-Z][a-zA-Z0-9+.-]*)://)?"
    r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):"
    r"(?P<port>\d{1,5})$"
)


def parse_ip_port(s: str):
    """
    Parse a string like 'tcp://147.250.140.85:7531' or '147.250.140.85:7531'.
    Returns (ip_address, port) or raises ValueError.
    """
    match = _PATTERN.match(s.strip())
    if not match:
        raise ValueError(f"'{s}' is not a recognizable ip:port string")

    ip_str = match.group("ip")
    port_str = match.group("port")

    # Validates octets are 0-255, not just digits
    ip = ipaddress.ip_address(ip_str)

    port = int(port_str)
    if not (0 <= port <= 65535):
        raise ValueError(f"port {port} out of range (0-65535)")

    return ip, port


def is_same_subnet(ip: ipaddress.IPv4Address, host_network: ipaddress.IPv4Network) -> bool:
    """Check whether ip belongs to host_network (e.g. 147.250.140.85/24)."""
    return ip in host_network


def get_local_network(prefix_len: int = 24) -> ipaddress.IPv4Network:
    """
    Best-effort way to find the host's own IP + assumed subnet,
    without needing to hardcode the interface.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # doesn't actually send anything
        local_ip = s.getsockname()[0]
        local_network = ipaddress.ip_network(f"{local_ip}/{prefix_len}", strict=False)
    return local_network


def validate_address(s: str) -> bool:
    try:
        ip, port = parse_ip_port(s)
    except ValueError:
        return False
    host_network = get_local_network()
    if host_network is not None and not is_same_subnet(ip, host_network):
        return False

    return True

if __name__ == "__main__":
    inputstrings = ['tcp://147.250.140.85:7531', '147.160.140.85:7531', 'tcp://147.0.140.85:7531', 'tcp://147.250.140.85:5555']
    for input in inputstrings:
        print(f'{input} is a valid address: {validate_address(input)}')