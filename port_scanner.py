import socket
import time
from datetime import datetime

ALLOWED_TARGETS = {"127.0.0.1", "localhost", "scanme.nmap.org"}

def parse_ports(port_input):
    port_input = port_input.strip()

    if "-" in port_input:
        start_str, end_str = port_input.split("-", 1)
        start = int(start_str)
        end = int(end_str)
        ports = list(range(start, end + 1))
    elif "," in port_input:
        parts = port_input.split(",")
        ports = [int(p.strip()) for p in parts]
    else:
        ports = [int(port_input)]

    for p in ports:
        if p < 1 or p > 65535:
            raise ValueError(f"Port {p} out of range.")
    return sorted(set(ports))

def scan_port(host, port, timeout=1.0):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0

def main():
    print("===== Python Port Scanner =====")
    print("Allowed targets: 127.0.0.1, localhost, scanme.nmap.org")
    target = input("Enter target host: ").strip()

    if target not in ALLOWED_TARGETS:
        print("[ERROR] Target not allowed by assignment rules.")
        print("       You may only scan: 127.0.0.1, localhost, scanme.nmap.org")
        return

    port_input = input("Enter ports (e.g. '22,80,443' or '20-1024'): ").strip()

    try:
        ports = parse_ports(port_input)
    except ValueError as exc:
        print(f"[ERROR] Invalid port input: {exc}")
        return

    print(f"\n[INFO] Starting scan of {target}")
    print(f"[INFO] Ports to scan: {ports}")
    start_time = datetime.now()
    print(f"[INFO] Start time: {start_time}")

    open_ports = []
    closed_ports = []

    try:
        for port in ports:
            try:
                if scan_port(target, port):
                    print(f"[OPEN ] Port {port} is OPEN")
                    open_ports.append(port)
                else:
                    print(f"[CLOSED] Port {port} is CLOSED or FILTERED")
                    closed_ports.append(port)
            except Exception as exc:
                print(f"[ERROR] Error scanning port {port}: {exc}")

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[SCAN] Interrupted.")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n===== Scan Summary =====")
    print(f"Target: {target}")
    print(f"Total ports scanned: {len(ports)}")
    print(f"Open ports: {open_ports if open_ports else 'None'}")
    print(f"Closed/filtered ports: {len(closed_ports)}")
    print(f"Start time: {start_time}")
    print(f"End time:   {end_time}")
    print(f"Duration:   {duration:.2f} seconds")
    print("=========================")

if __name__ == "__main__":
    main()
