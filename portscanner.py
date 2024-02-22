import socket

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  
            s.connect((ip, port))
            print(f"{port} is open")
    except:
        pass  

if __name__ == "__main__":
    target = "www.google.com"
    target_ip = socket.gethostbyname(target)
    print(f"Starting scan on host: {target_ip}")
    
    for port in range(1, 655335): 
        scan_port(target_ip, port)