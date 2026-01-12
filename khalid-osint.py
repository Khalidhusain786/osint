import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

# Forensic & Reporting (Legacy All Preserved)
try:
    import pdfkit
except ImportError:
    pass

init(autoreset=True)

# No Deletion Policy: Piche ka ek bhi logic delete nahi hua
found_data_for_pdf = []

def start_tor():
    """Tor service logic (v1-v41 Legacy Integrated)"""
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start")
        time.sleep(2)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def verify_link(url):
    """Naya Verification Logic: Fake data hatane ke liye (v39 logic)"""
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        return r.status_code == 200
    except: return False

def run_tool_verified(cmd, name, report_file):
    """V1-V42: Sabhi tools ki execution lines intact hain."""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                match = re.search(r'(https?://\S+)', clean_line)
                if match:
                    url = match.group(1).rstrip(']')
                    if verify_link(url):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.YELLOW}➤ {name}: {Fore.WHITE}{url}")
                        f.write(f"[{name}] {url}\n")
                        found_data_for_pdf.append(f"[{name}] {url}")
                elif any(x in clean_line.lower() for x in ["password:", "aadhar:", "voter:", "name:", "dob:"]):
                    if not any(bad in clean_line.lower() for bad in ["checking", "waiting"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"[{name}] {clean_line}\n")
                        found_data_for_pdf.append(f"[{name}] {clean_line}")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - THE ETERNAL FIXED MASTER v42.0            ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (User/Email/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # ALL PREVIOUS TOOLS (Zero Deletion Policy)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter"),
        (f"holehe {target} --only-used", "Email-Lookup"),
        (f"maigret {target} --timeout 20", "Identity-Mapper"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"truecallerpy search --number {target}", "Truecaller-Identity")
    ]

    print(f"{Fore.BLUE}[*] Crawling & Verifying Every Single Link... NO LINE DELETED:\n")
    threads = [Thread(target=run_tool_verified, args=(cmd, name, report_path)) for cmd, name in tools]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"\n{Fore
