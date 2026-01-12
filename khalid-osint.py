import os, subprocess, requests, time
from colorama import Fore, init

init(autoreset=True)

# --- CONFIGURATION ---
# Note: Agar API nahi hai, toh Telegram logic background mein silent rahega.
API_ID = 1234567  # Placeholder numeric ID
API_HASH = 'YOUR_API_HASH'
BOTS = ['osint_bot_link', 'breacheddatabot', 'HiTeck_Checker_bot', 'Hiddnosint_bot']

def run_engine_silent(cmd, name, target):
    """Faltu usage manual aur errors ko hide karne ke liye"""
    try:
        # Background mein run karein aur sirf output capture karein
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        combined_output = proc.stdout + proc.stderr
        
        # Sirf wahi lines nikaalein jismein real data ho
        findings = []
        for line in combined_output.split('\n'):
            # Filtering: 'Found', 'http', 'Name' jaise keywords par hi show karega
            if any(k in line.lower() for k in ["found", "http", "name:", "father:", "address:"]):
                if "error" not in line.lower() and "usage:" not in line.lower():
                    findings.append(line.strip())
        
        if findings:
            print(f"{Fore.GREEN}\n[✔] {name.upper()} DATA FOUND:")
            report_path = f"reports/{target}_data.txt"
            with open(report_path, "a") as f:
                f.write(f"\n--- {name} ---\n")
                for item in findings:
                    print(f"{Fore.WHITE}  ➤ {item}")
                    f.write(item + "\n")
            return True
    except:
        pass
    return False

def main():
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID ULTIMATE OSINT FRAMEWORK (FIXED)        ")
    print(f"{Fore.RED}======================================================")
    
    if not os.path.exists('reports'): os.makedirs('reports')

    target = input(f"\n{Fore.YELLOW}[+] Enter Target (Phone/User/Email): ")
    print(f"{Fore.CYAN}[*] Searching... (Sirf found data hi show hoga)\n")

    # 1. Maigret Fix: '--brief' ko hata kar silent mode use kiya hai
    run_engine_silent(f"maigret {target} --no-progress", "Maigret", target)
    
    # 2. Holehe (Email Scan)
    run_engine_silent(f"holehe {target} --only-used", "Holehe", target)
    
    # 3. Sherlock
    run_engine_silent(f"sherlock {target} --timeout 1 --print-found", "Sherlock", target)

    # 4. Google Gov Mirrors (For Name/Document search)
    run_engine_silent(f"googler --nocolor -n 3 -w gov.in \"{target}\"", "Gov-Records", target)

    print(f"\n{Fore.GREEN}================ SCAN FINISHED ================")
    print(f"{Fore.BLUE}Agar data mila hai toh 'reports/' folder mein check karein.")

if __name__ == "__main__":
    main()
