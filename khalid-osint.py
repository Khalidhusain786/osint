import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Anish Portal - First Priority
P_URL = "https://anishexploits.site/app/"
ACCESS_KEY = "Anish123"

def anish_portal_priority(target, report_file):
    """Auto-fills key and target, then scrapes data"""
    print(f"\n{Fore.RED}[PRIORITY #1] {Fore.CYAN}Accessing Anish Portal Database...")
    try:
        # Auto-submit payload
        data = {'access_key': ACCESS_KEY, 'number': target, 'submit': 'CHECK NOW'}
        response = requests.post(P_URL, data=data, timeout=12)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator="\n").strip()
            # Identifying key fields
            fields = ["Name", "Father", "Address", "Circle", "Aadhar", "Number :"]
            results = [line.strip() for line in text.split('\n') if any(f in line for f in fields)]
            
            if results:
                print(f"{Fore.GREEN}--- [ PORTAL DATA FOUND ] ---")
                for r in results: print(f"{Fore.WHITE}{r}")
                with open(report_file, "a") as f: f.write("\n--- ANISH PORTAL ---\n" + "\n".join(results) + "\n")
            else:
                print(f"{Fore.RED}[!] Portal: No record found for {target}.")
    except:
        print(f"{Fore.RED}[!] Portal: Connection failed.")

def stream_found(cmd, tool, target, report_file):
    """Filters only active profile links"""
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in proc.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool}: {line.strip()}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID OSINT - ANISH PORTAL PRIORITY EDITION")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User): ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # Run Priority #1
    anish_portal_priority(target, report_path)
    
    # Run Other Tools
    print(f"\n{Fore.BLUE}[*] Scanning Secondary OSINT Modules (Found-Only)...\n")
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret")
    ]
    
    for cmd, name in tools:
        stream_found(cmd, name, target, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Finished! Results saved at: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
