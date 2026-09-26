import socket
import sys
from datetime import datetime

def check_port(host, port, timeout=1.0):
    """
    Attempt a TCP connect to (host, port).
    Returns 'Open', 'Closed', or 'Filtered'.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            return "Open"
        else:
            # connect_ex returns an errno; most "refused" errors mean Closed
            return "Closed"
    except socket.timeout:
        return "Filtered"  # no response within timeout -> likely filtered by firewall
    except socket.gaierror:
        print(f"Hostname could not be resolved: {host}")
        sys.exit(1)
    except socket.error:
        return "Filtered"
    finally:
        sock.close()

def grab_banner(host, port, timeout=1.0):
    """Try to read a service banner for basic responsiveness info."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            try:
                banner = s.recv(1024).decode(errors="ignore").strip()
                return banner if banner else "No banner"
            except socket.timeout:
                return "No response"
    except Exception:
        return "N/A"

def scan_ports(host, start_port, end_port, timeout=1.0, grab_banners=False):
    print(f"\nScanning {host} from port {start_port} to {end_port}")
    print(f"Started at: {datetime.now()}\n")
    print(f"{'PORT':<10}{'STATUS':<12}{'SERVICE INFO'}")
    print("-" * 50)

    results = {"Open": [], "Closed": [], "Filtered": []}

    for port in range(start_port, end_port + 1):
        status = check_port(host, port, timeout)
        results[status].append(port)

        service_info = ""
        if status == "Open" and grab_banners:
            service_info = grab_banner(host, port, timeout)

        print(f"{port:<10}{status:<12}{service_info}")

    print("\nSummary:")
    print(f"  Open ports:     {results['Open']}")
    print(f"  Closed ports:   {len(results['Closed'])} ports")
    print(f"  Filtered ports: {results['Filtered']}")

    return results

if __name__ == "__main__":
    target_host = input("Enter target host (IP or hostname): ").strip()
    port_range = input("Enter port range (e.g., 1-100): ").strip()

    try:
        start_str, end_str = port_range.split("-")
        start_port, end_port = int(start_str), int(end_str)
    except ValueError:
        print("Invalid port range format. Use e.g. 20-100")
        sys.exit(1)

    timeout_input = input("Enter timeout in seconds (default 1.0): ").strip()
    timeout_val = float(timeout_input) if timeout_input else 1.0

    banner_choice = input("Attempt to grab service banners for open ports? (y/n): ").strip().lower()
    grab_banners = banner_choice == "y"

    scan_ports(target_host, start_port, end_port, timeout_val, grab_banners)
