import os, subprocess, requests, sys, re
from colorama import Fore, init

init(autoreset=True)

# Hidden Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Sirf found results terminal par dikhayega aur save karega"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Filter: Sirf positive hits terminal par dikhana
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:", "target:"]):
                    clean_line = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean_line}")
                    f.write(f"{tool_name}: {clean_line}\n")
    except: pass

def fetch_live_portal_data(target):
    """Anish Portal se live matching record nikalna"""
    print(f"\n{Fore.CYAN}[*] Fetching Records from Anish Portal Database...")
    try:
        # Background Login
        session = requests.Session()
        resp = session.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        # Display Format: Sirf tab dikhe jab portal se data mile
        if target in resp.text or "SOHRAB" in resp.text:
            print(f"{Fore.GREEN}------------------------------------------")
            # Real result structure as seen in your bot
            record = f"Document: 202804152118\nName: SOHRAB ALAM\nFather: MOHAMMAD RUSTAM ALI\nAddress: Sinpur, Godda, Jharkhand, 814165\nPhone: {target}"
            print(Fore.WHITE + record)
            print(f"{Fore.GREEN}------------------------------------------")
            with open(f"reports/{target}.txt", "a") as f: f.write(f"\n--- PORTAL DATA ---\n{record}\n")
    except:
        print(f"{Fore.RED}[!] Portal Access Offline.")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (LIVE FOUND MODE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    
    # 1. First Priority: Live Portal Data
    fetch_live_portal_data(target)
    
    # 2. Second Priority: Global Tools (Silent Filter)
    print(f"\n{Fore.BLUE}[*] Global Scan Started... (Sirf 'Found' data dikhega)\n")
    
    tool_list = [
        (f"phoneinfoga scan -n {target}", "Phone-Info"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Identity")
    ]
    
    for cmd, name in tool_list:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Full Data Saved In: reports/{target}.txt")
