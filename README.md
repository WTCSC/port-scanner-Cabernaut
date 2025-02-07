Overview
This Python script scans a network range specified in CIDR notation and reports the status of each host. It uses the ping command to check if hosts are up or down and provides a summary of the scan results. Additionally, the script can scan for open ports on hosts that are UP, allowing for network diagnostics and security checks.

Features
 Takes a CIDR notation input (e.g., 192.168.1.0/24)
 Calculates the network range based on the subnet mask
 Iterates over all valid host addresses in the range
 Reports which IP addresses successfully respond to ping requests
 Displays response time in milliseconds
 Provides a summary of active, down, and error hosts
 Supports port scanning (-p option) on hosts that are UP
 Scans individual ports, ranges, or multiple ports (e.g., -p 80, -p 1-100, -p 80,443,3306)
 Displays only open ports for clarity

Requirements
Python 3.x
ipaddress module (built-in with Python 3.3+)
Installation
No additional dependencies are required beyond Python. Simply clone this repository and run the script.

Usage
Basic Network Scan
To scan a network for active hosts, use:

bash
Copy
Edit
python ip_scanner.py 192.168.1.0/24
Example Output:
nginx
Copy
Edit
Scanning network 192.168.1.0/24...

192.168.1.1   (UP)
192.168.1.2   (DOWN)
192.168.1.3   (UP)
192.168.1.4   (UP)

Scan complete. Found 3 active hosts, 1 down, 0 errors.
Scanning for Open Ports
To scan for open ports on UP hosts, use the -p option:

Scan a single port (e.g., port 80):
bash
Copy
Edit
python ip_scanner.py -p 80 192.168.1.0/24
Scan a range of ports (e.g., 1-100):
bash
Copy
Edit
python ip_scanner.py -p 1-100 192.168.1.0/24
Scan multiple specific ports (e.g., 80, 443, 3306):
bash
Copy
Edit
python ip_scanner.py -p 80,443,3306 192.168.1.0/24
Example Output with Port Scanning:
nginx
Copy
Edit
Scanning network 192.168.1.0/24...

192.168.1.10  (UP)
  - Port 80   (OPEN)
  - Port 443  (OPEN)
192.168.1.11  (DOWN)
192.168.1.12  (DOWN)
192.168.1.13  (UP)
  - Port 80   (OPEN)
  - Port 3306 (OPEN)

Scan complete. Found 2 active hosts, 2 down, 0 errors.
Error Handling and Timeout
Hosts that do not respond to ping are marked as DOWN.
Hosts that experience an unexpected error will be marked as ERROR.
Port scanning includes a 1-second timeout per port to prevent long delays.
Conclusion
This tool provides a lightweight and easy-to-use method for scanning networks and identifying open ports. It is useful for system administrators, security professionals, and network troubleshooting. 🚀