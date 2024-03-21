import socket # provides low level networking interface
import concurrent.futures #launching parallel tasks using a pool of threats
from argparse import ArgumentParser # parsing command line arguments

def scan_port(ip, port, timeout=0.5, scan_type='TCP'): # scans single port, contains params ip, port, timeout, scan_type
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if scan_type == 'TCP' else socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service_info = f"{socket.getservbyport(port, scan_type.lower())}" if scan_type == 'TCP' else "UDP service"
            print(f"IP: {ip}: Port {port} is open ({service_info})")
        sock.close()
    except Exception as e:
        pass  # Ignoring exceptions for faster scanning

def scan_ports(ip, start_port, end_port, timeout, scan_type):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port, timeout, scan_type)

def main(target_ips, start_port, end_port, timeout, scan_type):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:  
        executor.map(scan_ports, target_ips, [start_port]*len(target_ips), [end_port]*len(target_ips), [timeout]*len(target_ips), [scan_type]*len(target_ips)) # executor map is used to align the function scan_ports to take multiple worker threads

if __name__ == "__main__":
    parser = ArgumentParser(description='Port Scanner')
    parser.add_argument('targets', nargs='+', help='IP address(es) or hostname(s) to scan')
    parser.add_argument('--start-port', type=int, default=1, help='Start of port range')
    parser.add_argument('--end-port', type=int, default=1024, help='End of port range')
    parser.add_argument('--timeout', type=float, default=0.5, help='Timeout for each port scan in seconds')
    parser.add_argument('--scan-type', choices=['TCP', 'UDP'], default='TCP', help='Type of scan: TCP or UDP')

    args = parser.parse_args()

    target_ips = []
    for target in args.targets:
        try:
            target_ip = socket.gethostbyname(target)
            target_ips.append(target_ip)
        except socket.gaierror:
            print(f"Hostname could not be resolved: {target}")

    if target_ips:
        main(target_ips, args.start_port, args.end_port, args.timeout, args.scan_type)
