import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Config - Priority #1
P_URL = "https://anishexploits.site/app/"
ACCESS_KEY = "Anish123"

def anish_portal_fixed(target, report_file):
    """Bypasses key and extracts data correctly even if structure changes"""
    print(f"\n{Fore.RED}[PRIORITY #1] {Fore.CYAN}Accessing Anish Portal Database...")
    try:
        # Number auto-submit logic
        payload = {'access_key': ACCESS_KEY, 'number': target, 'submit': 'CHECK NOW'}
        response = requests.post(P_URL, data=payload, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Catching the entire result block
            results_found = []
            for item in soup.find_all(['li', 'p', 'div']):
                text = item.get_text().strip()
                # Specific keywords check as seen in your screenshot
                if any(k in text for k in ["Number :", "Name :", "Father :", "Address :", "Circle :", "Aadhar :"]):
                    results_found.append(text)

            if results_found:
                print(f"{Fore.GREEN}--- [ REAL DATA FOUND FROM PORTAL ] ---")
                # Cleaning and printing each found line
                unique_results = list(dict.fromkeys(results_found)) # Remove duplicates
                for r in unique_results:
                    print(f"{Fore.WHITE}{r}")
                    with open(report_file, "a") as f: f.write(f"{r}\n")
                print(f"{Fore.GREEN}---------------------------------------")
            else:
                print(f"{Fore.RED}[!] Portal Search finished, but no readable data caught.")
    except Exception as e:
        print(f"{Fore.RED}[!] Connection Error with Portal.")

def stream_found_only(cmd, tool_name, target, report_file):
    """Filters results to show ONLY 'Found' links"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Showing only active links
                if any(x in line.lower() for x in ["http", "found", "[+]", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line.strip()}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (PORTAL DATA EXTRACTION FIXED)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User): ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # 1. Anish Portal First (Fixed Logic)
    anish_portal_fixed(target, report_path)
    
    # 2. Global OSINT Scan
    print(f"\n{Fore.BLUE}[*] Scanning Secondary Databases... (Found-Only Mode)\n")
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Report: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
