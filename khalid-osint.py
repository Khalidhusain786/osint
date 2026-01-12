import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread, Lock

init(autoreset=True)
all_raw_findings = []
print_lock = Lock()

# SOCKS5 Proxy for TOR
proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")
        time.sleep(1)
    print(f"{Fore.GREEN}[OK] Infrastructure Engine: ONLINE")

def shodan_iot_engine(target, report_file):
    """
    V58: Shodan IoT Recon. 
    Dhoondhta hai agar target ka IP ya Domain kisi vulnerable device se juda hai.
    """
    # Note: Shodan CLI or public dorks are used to avoid API dependency issues
    cmd = f"shodan search --limit 5 {target}"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            if any(x in line for x in [".", ":", "200"]):
                with print_lock:
                    print(f"{Fore.MAGENTA}[SHODAN-IOT] {Fore.WHITE}{line.strip()}")
                    all_raw_findings.append(f"Shodan: {line.strip()}")
    except: pass

def run_local_tool(cmd, name, report_file):
    """Runs high-intel local tools like Amass and theHarvester"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            clean = line.strip()
            # AI Logic: Only show 'Found' or actual data hits
            if any(x in clean.lower() for x in ["http", "found", "user", "@", "ip:"]):
                if not any(bad in clean.lower() for bad in ["searching", "checking", "trying"]):
                    with print_lock:
                        print(f"{Fore.GREEN}[FOUND] {Fore.YELLOW}{name}: {Fore.WHITE}{clean}")
                        all_raw_findings.append(f"{name}: {clean}")
                        with open(report_file, "a") as f: f.write(f"[{name}] {clean}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - INFRASTRUCTURE & HEAVY INTEL v58.0      ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/Domain/Username): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Defined Advanced Toolset
    tools = [
        (f"sherlock {target} --timeout 15", "Sherlock"),
        (f"maigret {target} --timeout 15", "Maigret"),
        (f"python3 whatsmyname.py -u {target}", "WhatsMyName"),
        (f"theHarvester -d {target} -l 100 -b google", "theHarvester"),
        (f"amass enum -d {target}", "Amass-DNS")
    ]

    print(f"{Fore.BLUE}[*] Launching Heavy Recon & IoT Scans...\n")

    # Start Shodan in separate thread
    Thread(target=shodan_iot_engine, args=(target, report_path)).start()

    # Launch Heavy Tools in parallel
    threads = [Thread(target=run_local_tool, args=(cmd, name, report_path)) for cmd, name in tools]
    
    for t in threads: t.start()
    for t in threads: t.join()

    print(f"\n{Fore.GREEN}[➔] Infrastructure Scan Done. Total Intel Hits: {len(all_raw_findings)}")

if __name__ == "__main__":
    main()
