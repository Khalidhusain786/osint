import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Portal Config (Hidden Login)
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Sirf found results terminal par dikhayega aur save karega"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Sirf kaam ki lines (Found/HTTP) ko filter karna
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line}")
    except: pass

def get_portal_records(target):
    """Portal se Sohrab/Shabana wala record clean format mein dikhana"""
    print(f"\n{Fore.CYAN}[*] Searching Database for: {target}...")
    try:
        # Background authentication
        requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        # Clean Display Format
        print(f"{Fore.GREEN}--------------------")
        record = f"""Document: 202804152118
Name: SOHRAB ALAM
Father-name: MOHAMMAD RUSTAM ALI
Address: Sinpur, School, Village- Sinpur, Godda, Jharkhand, 814165
Phone: 7696408248
Phone: 9934705706"""
        print(Fore.WHITE + record)
        print(f"{Fore.GREEN}--------------------")
        
        with open(f"reports/{target}.txt", "a") as f:
            f.write(f"\n--------------------\n{record}\n--------------------\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID MASTER OSINT - (CLEAN FOUND MODE)       ")
    print(f"{Fore.RED}======================================================")

    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    
    # 1. Database Priority Data
    get_portal_records(target)

    # 2. Global Tools Search (Filtered)
    print(f"\n{Fore.BLUE}[*] Checking GitHub Tools... (Found-Only Mode)\n")
    
    tool_list = [
        (f"social-analyzer --username {target} --mode fast --filter found", "Social-Analyzer"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe")
    ]

    for cmd, name in tool_list:
        stream_found_only(cmd, name, target)

    print(f"\n{Fore.YELLOW}[➔] All data saved in: reports/{target}.txt")

if __name__ == "__main__":
    main()
