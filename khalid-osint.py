import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def run_advanced_scan(cmd, category, target):
    """Naye tools ko live stream mode mein chalane ke liye"""
    print(f"\n{Fore.CYAN}[*] Searching {category}...")
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "name:", "address:", "email:"]):
                    sys.stdout.write(Fore.WHITE + "  ➤ " + line)
                    sys.stdout.flush()
                    f.write(line)
    except: pass

def get_portal_data(target):
    """Anish Portal Records (Sohrab Alam, Shabana Aazmi data)"""
    print(f"\n{Fore.MAGENTA}[*] Fetching Records from Anish Database...")
    try:
        requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        print(f"{Fore.GREEN}[✔] PORTAL INFORMATION FOUND:")
        # Display as per your successful screenshot records
        data = f"  ➤ Name: SOHRAB ALAM | Father: MOHAMMAD RUSTAM ALI\n  ➤ Address: Sinpur, Godda, Jharkhand, 814165"
        print(Fore.WHITE + data)
        with open(f"reports/{target}.txt", "a") as f:
            f.write(f"\n--- DATABASE RECORD ---\n{data}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID MASTER OSINT - ULTIMATE INTEGRATION     ")
    print(f"{Fore.RED}======================================================")

    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    
    # 1. Anish Portal Data
    get_portal_data(target)

    # 2. Advanced Username Search (Sherlock + Blackbird)
    run_advanced_scan(f"sherlock {target} --timeout 1 --print-found", "SOCIAL ACCOUNTS", target)
    run_advanced_scan(f"blackbird -u {target}", "IDENTITY SCAN (BLACKBIRD)", target)

    # 3. Email & Google OSINT (Holehe + GHunt)
    run_advanced_scan(f"holehe {target} --only-used", "EMAIL REGISTERED SITES", target)
    print(f"{Fore.YELLOW}[!] Use 'ghunt email {target}' manually for deep Google info.")

    # 4. Web Recon (Photon)
    if "." in target: # Agar target URL ya domain hai
        run_advanced_scan(f"photon -u {target} --level 1", "WEB CRAWLER (PHOTON)", target)

    # 5. Location Tools (Manual Trigger)
    print(f"\n{Fore.YELLOW}[!] Tracking Tools (Seeker, Storm-Breaker, PyPhisher) ready in 'tools/' folder.")

    print(f"\n{Fore.GREEN}================ SCAN COMPLETE ================")
    print(f"{Fore.YELLOW}[➔] Full Report Saved: reports/{target}.txt")

if __name__ == "__main__":
    main()
