import psutil
import platform
import socket
import threading
import time

# Suspicious process names (expand this list)
SUSPICIOUS_PROCESSES = ["keylogger", "pynput", "keyboard", "hook", "log_keys"]
SAFE_PROCESSES = ["gsd-keyboard", "xorg", "gnome-shell", "systemd", "bash"]
SAFE_APPS = ["chrome", "firefox", "edge", "brave", "code", "bash", "kdeconnectd", "gnome-software"]

# SMTP Ports for sending emails
SMTP_PORTS = {25, 465, 587}

def system_info():
    """Prints system details (OS, hostname, IP, MAC address)."""
    os_info = platform.system()
    hostname = socket.gethostname()

    # Get actual external IP
    ip_address = "Unknown"
    try:
        for interface, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                if addr.family == socket.AF_INET and addr.address != "127.0.0.1":
                    ip_address = addr.address  # Get non-loopback IP
                    break
    except:
        pass  

    # Get MAC address
    mac_address = "Unknown"
    try:
        for interface, addresses in psutil.net_if_addrs().items():
            for addr in addresses:
                if addr.family == psutil.AF_LINK:
                    mac_address = addr.address
    except:
        pass  

    print("\n[+] System Info:")
    print(f"    OS: {os_info}")
    print(f"    Hostname: {hostname}")
    print(f"    IP Address: {ip_address}")
    print(f"    MAC Address: {mac_address}\n")


def detect_keyboard_hooks():
    """Detects keylogger processes running in the background."""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            process_name = proc.info['name'].lower()
            if any(name in process_name for name in SUSPICIOUS_PROCESSES) and process_name not in SAFE_PROCESSES:
                print(f"[!] Suspicious keylogger process detected: {process_name} (PID: {proc.info['pid']})")
                return True
    except Exception as e:
        print(f"[Error] Could not scan processes: {e}")
    return False


def detect_network_activity():
    """Detects suspicious network activity."""
    suspicious_connections = []

    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_ESTABLISHED:
            try:
                process = psutil.Process(conn.pid)
                process_name = process.name().lower()
                remote_ip = conn.raddr.ip if conn.raddr else "Unknown"

                # Ignore safe apps
                if not any(proc in process_name for proc in SAFE_APPS):
                    suspicious_connections.append(f"{process_name} → {remote_ip}")
                    print(f"[!] Suspicious network activity: {process_name}(PID: {conn.pid}) → {remote_ip}")

            except:
                pass
    
    return suspicious_connections


def real_time_smtp_monitor():
    """Real-time monitoring of SMTP connections."""
    print("[M] Real-time SMTP Monitoring Started...\n")
    while True:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == psutil.CONN_ESTABLISHED:
                try:
                    process = psutil.Process(conn.pid)
                    process_name = process.name().lower()
                    remote_ip = conn.raddr.ip if conn.raddr else "Unknown"
                    remote_port = conn.raddr.port if conn.raddr else 0

                    if remote_port in SMTP_PORTS:
                        print(f"[M] Email Sending Detected: {process_name} → {remote_ip}:{remote_port}")
                except:
                    pass
        time.sleep(0.5)  # Check every 0.5 seconds


# Show system info before scanning
system_info()

# Start real-time SMTP monitoring in a separate thread
smtp_thread = threading.Thread(target=real_time_smtp_monitor, daemon=True)
smtp_thread.start()

print("[+] Keylogger & SMTP Detector Running...\n")

n = 0
while True:
    detected = detect_keyboard_hooks()
    network_issues = detect_network_activity()

    if detected or network_issues:
        print("[!] Warning: Suspicious activity detected! ["+time.strftime("%A %Y-%m-%d %H:%M:%S")+"]\n")
        n = 0
    else:
        if n == 0:
            n = 1
            print("[*] No suspicious activity detected.")
            

    time.sleep(5)  # Scan every 5 seconds
