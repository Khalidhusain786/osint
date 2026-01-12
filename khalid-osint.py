import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Config
P_URL = "https://anishexploits.site/app/"
ACCESS_KEY = "Anish123"

def portal_auto_bypass(target, report_file):
    """Anish Portal: Auto-Key & Auto-Search"""
    print(f"\n{Fore.CYAN}[*] Bypassing Anish Portal (Key: {ACCESS_KEY})...")
    try:
        # Number auto-fill aur check now auto-click logic
        payload = {'access_key': ACCESS_KEY, 'number': target, 'submit': 'CHECK NOW'}
        resp = requests.post(P_URL, data=payload, timeout=15)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            clean_text = soup.get_text(separator="\n").strip()
            # Extracting only useful data
            keys = ["Name", "Father", "Address", "Circle", "Aadhar", "Number :"]
            found_data = [l.strip() for l in clean_text.split('\n') if any(k in l for k in keys)]
            
            if found_data:
                print(f"{Fore.GREEN}--- [ PORTAL: DATA FOUND ] ---")
                for item in found_data: print(f"{Fore.WHITE}{item}")
                with open(report_file, "a") as f: f.write("\n--- PORTAL DATA ---\n" + "\n".join(found_data) + "\n")
            else:
                print(f"{Fore.RED}[!] PORTAL: No Data Found for {target}.")
    except Exception: print(f"{Fore.RED}[!] Portal offline or Key failed.")

def stream_found_only(cmd, tool_name, target, report_file):
    """Terminal par kachra aur errors filter karna"""
    try:
        # Errors ko hide karne ke liye stderr=DEVNULL use kiya hai
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    clean_line = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean_line}")
                    f.write(f"{tool_name}: {clean_line}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (ZERO ERROR & AUTO-BYPASS MODE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # 1. Portal Auto-Search
    portal_auto_bypass(target, report_path)
    
    # 2. Scanning with All 30+ Tools (Full List Protected)
    print(f"\n{Fore.BLUE}[*] Running All Modules (Found-Only Mode)...\n")
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer"),
        (f"holehe {target} --only-used", "Holehe-Email"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"blackbird -u {target}", "SocialLinks")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] All Results Saved. Path: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
