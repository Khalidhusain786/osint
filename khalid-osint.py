import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Portal Configuration (Background Access)
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Sirf found results terminal par dikhayega aur save karega"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Filter logic: Sirf valid hits terminal par dikhana
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    clean_line = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean_line}")
                    f.write(f"{tool_name}: {clean_line}\n")
    except: pass

def get_portal_data(target):
    """Anish Portal se live data fetch karna"""
    print(f"\n{Fore.CYAN}[*] Fetching Records from Anish Portal Database...")
    try:
        session = requests.Session()
        resp = session.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        # Sirf tabhi save karein agar portal se kuch real data mile
        if resp.status_code == 200 and len(resp.text) > 10:
            print(f"{Fore.GREEN}--- [ REAL DATA FOUND ] ---")
            print(Fore.WHITE + resp.text.strip())
            print(f"{Fore.GREEN}---------------------------")
            with open(f"reports/{target}.txt", "a") as f: 
                f.write(f"\n--- LIVE PORTAL DATA ---\n{resp.text}\n")
    except:
        print(f"{Fore.RED}[!] Portal Access Error.")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (LIVE SCAN & AUTO-OPEN)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/Email/User): ")
    report_path = f"reports/{target}.txt"
    
    # 1. Start Anish Portal Access
    get_portal_data(target)
    
    # 2. Start Multi-Tool Scan (Found Only)
    print(f"\n{Fore.BLUE}[*] Scanning Global Databases... (Sirf 'Found' results)\n")
    
    tools = [
        (f"phoneinfoga scan -n {target}", "Phone-Info"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe Email"),
        (f"maigret {target} --timeout 10", "Identity")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Opening report: {report_path}")
    
    # Auto-Open Report in Mousepad (Kali default text editor)
    os.system(f"mousepad {report_path} &")
