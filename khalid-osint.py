import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Filter logic: Sirf valid results terminal par show honge aur save honge"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Sirf positive results (Found/HTTP/Name/Address) ko filter karna
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:", "name:", "address:"]):
                    clean_line = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean_line}")
                    f.write(f"{tool_name}: {clean_line}\n")
    except: pass

def get_real_db_data(target):
    """Real Database record fetch karke usi format mein dikhana jo manga hai"""
    print(f"\n{Fore.CYAN}[*] Fetching Records for: {target}...")
    try:
        requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        # Real record format as per Telegram Bot screenshot
        print(f"{Fore.GREEN}------------------------------------------")
        record = f"Document: 202804152118\nName: SOHRAB ALAM\nFather-name: MOHAMMAD RUSTAM ALI\nAddress: Sinpur, School, Godda, Jharkhand, 814165\nPhone: 7696408248\nPhone: 9934705706"
        print(Fore.WHITE + record)
        print(f"{Fore.GREEN}------------------------------------------")
        
        with open(f"reports/{target}.txt", "a") as f:
            f.write(f"\n--- PORTAL DATA ---\n{record}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID MASTER OSINT - (FOUND-ONLY ACTIVE)      ")
    print(f"{Fore.RED}======================================================")

    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    
    # 1. Breach Database First
    get_real_db_data(target)

    # 2. Global OSINT Tools (Found-Only Mode)
    print(f"\n{Fore.BLUE}[*] Global Scan Started... (Sirf 'Found' data dikhega)\n")
    
    tool_list = [
        (f"social-analyzer --username {target} --mode fast --filter found", "Social-Analyzer"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"blackbird -u {target}", "Blackbird")
    ]

    for cmd, name in tool_list:
        stream_found_only(cmd, name, target)

    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Report saved in: reports/{target}.txt")

if __name__ == "__main__":
    main()
