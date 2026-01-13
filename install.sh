import os, subprocess, sys, requests, re, time
# ... (baaki imports same rakhein)

def start_tor():
    """Environment-aware Tor starter"""
    is_termux = os.path.exists("/data/data/com.termux/files/usr/bin")
    
    try:
        if is_termux:
            # Termux doesn't support systemctl, check if port 9050 is open
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 9050))
            if result != 0:
                print(f"{Fore.YELLOW}[!] ALERT: Tor is NOT running. Run 'tor' in another Termux tab.")
            sock.close()
        else:
            # Kali/Linux logic
            status = os.popen("systemctl is-active tor").read().strip()
            if status != "active":
                print(f"{Fore.YELLOW}[*] Starting Tor Service...")
                os.system("sudo service tor start > /dev/null 2>&1")
        
        print(f"{Fore.GREEN}[OK] Ghost Tunnel: HTTP/HTTPS/ONION PROTOCOLS ACTIVE")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Tor Check Failed: {e}")

def clean_and_verify(raw_html, target, report_file, source_label):
    try:
        # Fallback for lxml if not available
        try:
            soup = BeautifulSoup(raw_html, 'lxml')
        except:
            soup = BeautifulSoup(raw_html, 'html.parser')
        
        # ... (rest of the cleaning logic)
