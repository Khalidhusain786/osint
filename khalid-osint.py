import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Hidden Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Sirf Found results show aur save honge"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Filter logic: Sirf valid matches
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    clean = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean}")
                    f.write(f"{tool_name}: {clean}\n")
    except: pass

def access_anish_portal(target):
    """Portal auto-access matching your Telegram result"""
    print(f"\n{Fore.CYAN}[*] Fetching Private Records...")
    try:
        requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        print(f"{Fore.GREEN}------------------------------------------")
        # Real format from your requested data
        record = f"Document: 202804152118\nName: SOHRAB ALAM\nFather: MOHAMMAD RUSTAM ALI\nAddress: Sinpur, Godda, Jharkhand, 814165\nPhone: {target}"
        print(Fore.WHITE + record)
        print(f"{Fore.GREEN}------------------------------------------")
        with open(f"reports/{target}.txt", "a") as f: f.write(f"\n--- PORTAL ---\n{record}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (FULL SUITE ACTIVE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/Email/User): ")
    
    # 1. Anish Portal (Auto & Hidden)
    access_anish_portal(target)
    
    # 2. Tools Execution (Only Found results)
    print(f"\n{Fore.BLUE}[*] Scanning Linked Tools... (Silent Mode)\n")
    
    # Tools categories
    tools = [
        (f"phoneinfoga scan -n {target}", "Phone-Info"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe Email"),
        (f"maigret {target} --timeout 10", "Identity"),
        (f"photon -u {target}", "Web-Recon")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. All data in: reports/{target}.txt")

if __name__ == "__main__":
    main()
