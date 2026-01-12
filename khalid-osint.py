import os, subprocess, requests, time
from colorama import Fore, init

init(autoreset=True)

# Hidden Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def save_and_show(target, tool_name, cmd):
    print(f"\n{Fore.CYAN}[*] Initializing {tool_name} Scan...")
    report_path = f"reports/{target}.txt"
    
    try:
        # Tool execution
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        
        # Screen par dikhane ke liye logic
        if len(output.strip()) > 10:
            print(f"{Fore.GREEN}[✔] {tool_name} Data Found:")
            print(Fore.WHITE + output)
            
            # File mein save karne ke liye
            with open(report_path, "a") as f:
                f.write(f"\n{'='*20} {tool_name} RESULTS {'='*20}\n")
                f.write(output)
                f.write("\n\n")
        else:
            print(f"{Fore.RED}[-] No data found by {tool_name}")
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error in {tool_name}: {e}")

def main():
    # Folder setup
    if not os.path.exists('reports'): os.makedirs('reports')
    
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID PRIVATE MASTER OSINT FRAMEWORK (V8.0)    ")
    print(f"{Fore.RED}======================================================")
    
    # Hidden Auto-Login (Password screen par nahi dikhega)
    try:
        requests.post(P_URL, data={'password': P_KEY}, timeout=5)
        print(f"{Fore.GREEN}[✔] PORTAL STATUS: ACTIVE (HIDDEN LOGIN)")
    except:
        print(f"{Fore.YELLOW}[!] Portal Bypass Active")

    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Username/Email/Phone): ")
    
    print(f"\n{Fore.BLUE}[*] Full System Scan Shuru Ho Raha Hai. Sabr Karein...")
    
    # --- SARE TOOLS EK SAATH ---
    
    # 1. Sherlock (Social Media)
    save_and_show(target, "SHERLOCK", f"sherlock {target} --timeout 1 --print-found")
    
    # 2. Holehe (Email OSINT)
    save_and_show(target, "HOLEHE", f"holehe {target} --only-used")
    
    # 3. Maigret (Deep Web Social Search)
    save_and_show(target, "MAIGRET", f"maigret {target} --timeout 10")

    # 4. Custom Search (Agar tool installed hai)
    # save_and_show(target, "GOV-RECORDS", f"googler -n 5 {target}")

    print(f"\n{Fore.GREEN}================ SCAN
