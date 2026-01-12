import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Hidden Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Sirf Found results terminal par dikhayega aur save karega"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Filter logic: Sirf valid matches dikhana
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    clean_line = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean_line}")
                    f.write(f"{tool_name}: {clean_line}\n")
    except: pass

def get_live_portal_data(target):
    """Anish Portal se background mein live data fetch karna"""
    print(f"\n{Fore.CYAN}[*] Accessing Live Portal Database for: {target}...")
    try:
        session = requests.Session()
        resp = session.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        # Agar portal data return karta hai, tabhi dikhayega
        if resp.status_code == 200 and len(resp.text) > 50:
            print(f"{Fore.GREEN}--- [ REAL DATA FOUND ] ---")
            print(Fore.WHITE + resp.text.strip())
            print(f"{Fore.GREEN}---------------------------")
            with open(f"reports/{target}.txt", "a") as f: 
                f.write(f"\n--- LIVE PORTAL DATA ---\n{resp.text}\n")
    except:
        print(f"{Fore.RED}[!] Portal link failed.")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (LIVE & CLEAN MODE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/Email/User): ")
    
    # 1. Access Anish Portal (Auto-Access)
    get_live_portal_data(target)
    
    # 2. Run All OSINT Tools (Found Only)
    print(f"\n{Fore.BLUE}[*] Global Scan Started... (Sirf 'Found' data dikhega)\n")
    
    tool_list = [
        (f"phoneinfoga scan -n {target}", "Phone-Info"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe Email"),
        (f"maigret {target} --timeout 10", "Identity")
    ]
    
    for cmd, name in tool_list:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. All data in: reports/{target}.txt")
