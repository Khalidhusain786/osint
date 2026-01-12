import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Config - Priority #1
P_URL = "https://anishexploits.site/app/"
ACCESS_KEY = "Anish123"

def extract_portal_data(target, report_file):
    """Specifically targets data fields shown in portal"""
    print(f"\n{Fore.RED}[PRIORITY #1] {Fore.CYAN}Fetching Anish Portal Data...")
    try:
        # Step 1: Login & Search
        payload = {'access_key': ACCESS_KEY, 'number': target, 'submit': 'CHECK NOW'}
        response = requests.post(P_URL, data=payload, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extracting all text content to find matches
            page_text = soup.get_text(separator="\n")
            lines = [l.strip() for l in page_text.split('\n') if l.strip()]
            
            # Fields to catch
            targets = ["Number :", "Name :", "Father :", "Address :", "Circle :", "Aadhar :"]
            found = False
            
            print(f"{Fore.GREEN}--- [ DATA RESULTS ] ---")
            with open(report_file, "a") as f:
                for line in lines:
                    if any(t in line for t in targets):
                        print(f"{Fore.WHITE}{line}")
                        f.write(f"{line}\n")
                        found = True
            
            if not found:
                print(f"{Fore.RED}[!] Portal Search finished, but no readable data caught.")
    except:
        print(f"{Fore.RED}[!] Portal Connection Failed.")

def run_tool(cmd, name, report_file):
    """Silent execution - Only shows found results"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "link:"]):
                    print(f"{Fore.GREEN}[+] {name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{name}: {line.strip()}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (FULL FIXED EDITION)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # 1. Anish Portal (Priority)
    extract_portal_data(target, report_path)
    
    # 2. All Secondary Tools (No Removal)
    print(f"\n{Fore.BLUE}[*] Scanning Secondary Tools (Found-Only)...\n")
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer"),
        (f"blackbird -u {target}", "Blackbird")
    ]
    
    for cmd, name in tools:
        run_tool(cmd, name, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] Process Complete. Results: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
