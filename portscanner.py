import socket
import concurrent.futures

def scan_port(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout) # adding timeout for effiency
            result = s.connect_ex((ip, port))
            if result == 0: # 0 indicates a successful connection
                print(f"IP: {ip}: Port {port} is open")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
# had an issue where the port scans were extremely slow due to sequentially checking the ports
# resolved this with multithreaded port scanning using a thread pool executor
def main(target_ip): 
    threads = 750

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, target_ip, port) for port in range(1, 1025)]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in main execution: {e}")

if __name__ == "__main__":
    target = input("Enter the hostname or IP to scan: ")
    try:
        target_ip = socket.gethostbyname(target)
        print(f"Hostname IP address: {target_ip}")
        main(target_ip)
    except socket.gaierror:
        print(f"Hostname could not be resolved: {target}")
    except Exception as e:
        print(f"An error occurred: {e}")