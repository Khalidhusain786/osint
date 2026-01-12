import os, subprocess, requests
from colorama import Fore, init

init(autoreset=True)

def run_engine(cmd, name, target):
    """Errors ko background mein hide karke sirf Links/Data dikhana"""
    try:
        # Background run (No usage manual on screen)
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        
        # Filtering: Sirf tabhi print hoga jab real link ya data mile
        keywords = ["found", "http", "name:", "father:", "address:", "[+]"]
        findings = [l.strip() for l in out.split('\n') if any(k in l.lower() for k in keywords) and "usage:" not in l.lower() and "404" not in l]

        if findings:
            print(f"{Fore.GREEN}\n[✔] {name.upper()} RESULTS FOR {target}:")
            for item in findings:
                # Terminal mein clickable link banana
                if "http" in item:
                    print(f"{Fore.WHITE}  ➤ {item}")
                else:
                    print(f"{Fore.YELLOW}  ➤ {item}")
            return True
    except: pass
    return False

def main():
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID MASTER OSINT - ALL TOOLS LOADED         ")
    print(f"{Fore.RED}======================================================")
    
    target = input(f"\n{Fore.YELLOW}[+] Enter Target (User/Email/Phone): ")
    print(f"{Fore.CYAN}[*] Deep Scanning... (Sirf 'Found' data hi show hoga)\n")

    # --- CATEGORY 1: USERNAME (Sherlock/Maigret) ---
    run_engine(f"sherlock {target} --timeout 1 --print-found", "Social-Accounts", target)
    run_engine(f"maigret {target} --no-progress", "Deep-Social", target)

    # --- CATEGORY 2: EMAIL (Holehe/GHunt) ---
    run_engine(f"holehe {target} --only-used", "Email-Investigation", target)

    # --- CATEGORY 3: PHONE (PhoneInfoga Mirror) ---
    # Hum direct web-check karenge taaki API error na aaye
    google_link = f"https://www.google.com/search?q=site:*.in+\"{target}\""
    print(f"{Fore.GREEN}\n[✔] PHONE/NAME WEB SEARCH:")
    print(f"{Fore.WHITE}  ➤ {google_link}")

    # --- CATEGORY 4: GOV RECORDS (Googler) ---
    run_engine(f"googler --nocolor -n 3 -w gov.in \"{target}\"", "Gov-Records", target)

    print(f"\n{Fore.GREEN}================ SCAN COMPLETE ================")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    main()
