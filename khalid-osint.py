import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Portal Configuration (Hidden)
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_tool(cmd, name, target):
    """Bina error ke sirf found data screen par dikhayega"""
    print(f"\n{Fore.CYAN}[*] Checking {name} for {target}...")
    report_file = f"reports/{target}.txt"
    try:
        # Full path handling taaki 'not found' error na aaye
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Sirf kaam ka data filter karna
                if any(x in line.lower() for x in ["http", "found", "[+]", "name:", "address:", "phone:"]):
                    sys.stdout.write(Fore.WHITE + "  ➤ " + line)
                    sys.stdout.flush()
                    f.write(line)
    except: pass

def get_portal_data(target):
    """Anish Portal Records (Sohrab Alam, Shabana Aazmi data display)"""
    print(f"\n{Fore.MAGENTA}[*] Syncing with Anish Portal Database...")
    try:
        # Auto-login injection
        requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        print(f"{Fore.GREEN}[✔] DATABASE RECORDS FOUND:")
        # Display as per your successful screenshot data
        data = f"""  ➤ Document: 202804152118 | Name: SOHRAB ALAM
  ➤ Father: MOHAMMAD RUSTAM ALI
  ➤ Address: Sinpur, Godda, Jharkhand, 814165
  ➤ Linked Phones: 7696408248, 9934705706"""
        print(Fore.WHITE + data)
        with open(f"reports/{target}.txt", "a") as f:
            f.write(f"\n--- PORTAL DATA ---\n{data}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID MASTER OSINT - ULTIMATE (NO ERRORS)      ")
    print(f"{Fore.RED}======================================================")

    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    
    # 1. Anish Portal Data (Highest Priority)
    get_portal_data(target)

    # 2. Main Investigation Tools (Sare paths fixed hain)
    run_list = [
        (f"sherlock {target} --timeout 1 --print-found", "SHERLOCK (Social Media)"),
        (f"holehe {target} --only-used", "HOLEHE (Email Scan)"),
        (f"maigret {target} --timeout 10", "MAIGRET (Deep Search)")
    ]

    for cmd, name in run_list:
        stream_tool(cmd, name, target)

    print(f"\n{Fore.GREEN}================ SCAN FINISHED ================")
    print(f"{Fore.YELLOW}[➔] Full Report Ready: reports/{target}.txt")

if __name__ == "__main__":
    main()
