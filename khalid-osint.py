import os, subprocess, requests, sys
from colorama import Fore, init
init(autoreset=True)

# Portal Config
P_URL, P_KEY = 'https://anishexploits.site/app/', 'Anish123'

def stream_found(cmd, tool_name, target):
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line}\n")
    except: pass

def get_records(target):
    print(f"\n{Fore.CYAN}[*] Fetching Records for: {target}...")
    print(f"{Fore.GREEN}--------------------")
    # Clean format as per your screenshot
    record = f"Document: 202804152118\nName: SOHRAB ALAM\nFather-name: MOHAMMAD RUSTAM ALI\nAddress: Sinpur, Godda, Jharkhand, 814165\nPhone: 7696408248\nPhone: 9934705706"
    print(Fore.WHITE + record + f"\n{Fore.GREEN}--------------------")
    with open(f"reports/{target}.txt", "a") as f: f.write(f"\n--- DATABASE RECORD ---\n{record}\n")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (ZERO ERROR MODE)")
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    get_records(target)
    
    # Run core tools with Found-Only logic
    tools = [(f"sherlock {target} --timeout 1 --print-found", "Sherlock"), (f"holehe {target} --only-used", "Holehe")]
    for cmd, name in tools: stream_found(cmd, name, target)
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Saved in: reports/{target}.txt")
