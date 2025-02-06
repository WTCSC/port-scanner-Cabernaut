import argparse
import ipaddress
import subprocess
import platform
import time
import socket

# Function to ping a host and return its status and response time
def ping_host(ip):
    """Pings a host and returns its status and response time."""
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    try:
        start_time = time.time()
        result = subprocess.run(["ping", param, ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        end_time = time.time()
        
        if result.returncode == 0:
            return "UP", round((end_time - start_time) * 1000)  # Convert to milliseconds
        else:
            return "DOWN", "No response"
    except Exception as e:
        return "ERROR", str(e)

# Function to scan a range of ports on a host
def scan_ports(ip, ports):
    """Scans specified ports on a host and returns a list of open ports."""
    open_ports = []
    for port in ports:
        try:
            sock = socket.create_connection((ip, port), timeout=1)  # Timeout after 1 second
            open_ports.append(port)
            sock.close()
        except (socket.timeout, socket.error):
            continue
    return open_ports

# Function to parse the port argument
def parse_ports(port_arg):
    """Parses the port argument and returns a list of ports to scan."""
    ports = []
    for part in port_arg.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

# Function to scan the given network range and report active hosts
def scan_network(cidr, ports=None):
    """Scans the given network range and reports active hosts and open ports."""
    network = ipaddress.ip_network(cidr, strict=False)
    
    print(f"Scanning network {cidr}...\n")
    up_count = 0
    down_count = 0
    error_count = 0
    
    for ip in network.hosts():  # Iterate over all valid hosts in the network
        status, response = ping_host(str(ip))
        if status == "UP":
            print(f"{ip}  (UP)")
            up_count += 1
            if ports:
                open_ports = scan_ports(str(ip), ports)
                for port in open_ports:
                    print(f"  - Port {port}   (OPEN)")
        elif status == "DOWN":
            print(f"{ip}  (DOWN)")
            down_count += 1
        else:
            print(f"{ip}  (ERROR) - {response}")
            error_count += 1
    
    # Display scan summary
    print(f"\nScan complete. Found {up_count} active hosts, {down_count} down, {error_count} errors.")

# Main execution block to parse arguments and start scanning
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple IP Scanner with Port Scanning")
    parser.add_argument("cidr", help="CIDR notation (e.g., 192.168.1.0/24)")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., 80,443,3306 or 1-100)")
    args = parser.parse_args()

    if args.ports:
        ports = parse_ports(args.ports)
        scan_network(args.cidr, ports)
    else:
        scan_network(args.cidr)