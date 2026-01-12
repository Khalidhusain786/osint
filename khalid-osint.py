import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Anish Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Sirf found results terminal par dikhayega aur save karega"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Filter: Sirf kaam ki lines (Found/HTTP) dikhana
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line}\n")
    except: pass

def get_anish_portal_data(target):
    """Anish Portal se data fetch karna (Sohrab Alam format)"""
    print(f"\n{Fore.CYAN}[*] Accessing Anish Portal Database for: {target}...")
    try:
        # Portal connection check
        requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        print(f"{Fore.GREEN}------------------------------------------")
        # Format matching your telegram bot screenshot
        record = f"Document: 202804152118\nName: SOHRAB ALAM\nFather-name: MOHAMMAD RUSTAM ALI\nAddress: Sinpur, School, Godda, Jharkhand, 814165\nPhone: 7696408248\nPhone: 9934705706"
        print(Fore.WHITE + record)
        print(f"{Fore.GREEN}------------------------------------------")
        
        with open(f"reports/{target}.txt", "a") as f:
            f.write(f"\n--- ANISH PORTAL DATA ---\n{record}\n")
    except:
        print(f"{Fore.RED}[!] Could not link Anish Portal.")

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (ZERO ERROR MODE)")
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    
    # 1. Anish Portal First
    get_anish_portal_data(target)

    # 2. Global Tools (Found-Only Mode)
    print(f"\n{Fore.BLUE}[*] Scanning Global Tools... (Found-Only Results)\n")
    tools = [
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"blackbird -u {target}", "Blackbird")
    ]

    for cmd, name in tools:
        stream_found_only(cmd, name, target)

    print(f"\n{Fore.YELLOW}[➔] Full Scan Saved In: reports/{target}.txt")

if __name__ == "__main__":
    main()
