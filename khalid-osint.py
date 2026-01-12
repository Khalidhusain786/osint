import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Config
P_URL = "https://anishexploits.site/app/"
ACCESS_KEY = "Anish123"

def run_portal_first(target, report_file):
    """Anish Portal Priority Extraction"""
    try:
        payload = {'access_key': ACCESS_KEY, 'number': target, 'submit': 'CHECK NOW'}
        response = requests.post(P_URL, data=payload, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Labels shown in your portal screenshot
            labels = ["Number :", "Name :", "Father :", "Address :", "Circle :", "Aadhar :"]
            
            print(f"\n{Fore.GREEN}--- [ ANISH PORTAL: PRIORITY RESULTS ] ---")
            found = False
            with open(report_file, "a") as f:
                for tag in soup.find_all(['li', 'p', 'div', 'span']):
                    text = tag.get_text().strip()
                    if any(label in text for label in labels):
                        print(f"{Fore.WHITE}{text}")
                        f.write(f"{text}\n")
                        found = True
            if not found:
                print(f"{Fore.RED}[!] No matching identity labels found in portal.")
            print(f"{Fore.GREEN}------------------------------------------\n")
    except Exception:
        print(f"{Fore.RED}[!] Portal connection failed.")

def run_legacy_tools(cmd, name, report_file):
    """Runs all older tools without breaking"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Catching only useful 'Found' lines
                if any(x in line.lower() for x in ["http", "found", "[+]", "link:"]):
                    print(f"{Fore.CYAN}[+] {name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{name}: {line.strip()}\n")
    except Exception:
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID OSINT - FULL SYSTEM (PORTAL FIRST)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # 1. Anish Portal (Priority #1)
    run_portal_first(target, report_path)
    
    # 2. Complete Legacy Toolset (No Removal)
    print(f"{Fore.BLUE}[*] Running all secondary OSINT modules...\n")
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"blackbird -u {target}", "Blackbird"),
        (f"photon -u {target}", "Photon")
    ]
    
    for cmd, name in tools:
        run_legacy_tools(cmd, name, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete! Report: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
