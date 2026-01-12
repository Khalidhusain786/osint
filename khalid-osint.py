import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Configuration
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Filter logic: Sirf working links terminal par dikhana"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    clean_line = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean_line}")
                    f.write(f"{tool_name}: {clean_line}\n")
    except: pass

def get_clean_portal_data(target):
    """Anish Portal se HTML hatakar sirf saaf text dikhana"""
    print(f"\n{Fore.CYAN}[*] Fetching Clean Data from Portal...")
    try:
        session = requests.Session()
        resp = session.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        if resp.status_code == 200:
            # HTML Cleaner Logic
            soup = BeautifulSoup(resp.text, 'html.parser')
            clean_text = soup.get_text(separator="\n").strip()
            
            # Sirf relevant data dikhana (Purana Sohrab format delete)
            if len(clean_text) > 5:
                print(f"{Fore.GREEN}--- [ LIVE DATA FOUND ] ---")
                print(Fore.WHITE + clean_text)
                print(f"{Fore.GREEN}---------------------------")
                with open(f"reports/{target}.txt", "a") as f:
                    f.write(f"\n--- PORTAL DATA ---\n{clean_text}\n")
            else:
                print(f"{Fore.YELLOW}[!] No records found on portal.")
    except Exception as e:
        print(f"{Fore.RED}[!] Portal Access Error.")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (CLEAN TEXT MODE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    report_path = f"reports/{target}.txt"
    
    # 1. Access Portal & Clean HTML
    get_clean_portal_data(target)
    
    # 2. Global Scan (Found Only)
    print(f"\n{Fore.BLUE}[*] Scanning Global Databases... (Silent Mode)\n")
    tools = [
        (f"phoneinfoga scan -n {target}", "Phone-Info"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe Email"),
        (f"maigret {target} --timeout 10", "Identity")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Opening report...")
    os.system(f"mousepad {report_path} &")
