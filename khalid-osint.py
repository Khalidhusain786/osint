import os, subprocess, requests, time
from colorama import Fore, init

init(autoreset=True)

# --- AUTO-LOGIN CONFIG ---
LINK = "https://anishexploits.site/app/"
PASS = "Anish123"

def run_silent(cmd, name):
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        findings = [l.strip() for l in out.split('\n') if "http" in l.lower() and "404" not in l]
        if findings:
            print(f"{Fore.GREEN}\n[✔] {name.upper()} DATA FOUND:")
            for link in findings[:5]: print(f"{Fore.WHITE}  ➤ {link}")
    except: pass

def auto_auth_check():
    """Anish Exploits link ko auto-password se check karne ke liye"""
    print(f"{Fore.MAGENTA}[*] Connecting to AnishExploits Portal...")
    try:
        # Password auto-fill logic using payload
        payload = {'password': PASS} 
        r = requests.post(LINK, data=payload, timeout=10)
        if r.status_code == 200:
            print(f"{Fore.GREEN}[✔] Auto-Login Successful! Portal is Active.")
        else:
            print(f"{Fore.YELLOW}[!] Portal connected, but requires manual bypass.")
    except:
        print(f"{Fore.RED}[!] Link unreachable, skipping auto-auth.")

def main():
    os.system('clear')
    print(f"{Fore.RED}=== KHALID MASTER OSINT (AUTO-AUTH V7.0) ===")
    auto_auth_check() # Auto-password fill check
    
    target = input(f"\n{Fore.YELLOW}[+] Enter Target (Username/Email): ")
    print(f"{Fore.CYAN}[*] Searching... (Sirf 'Found' data hi dikhega)\n")

    # Core engines
    run_silent(f"sherlock {target} --timeout 1 --print-found", "Social Media")
    run_silent(f"holehe {target} --only-used", "Email Presence")
    
    print(f"\n{Fore.BLUE}[*] Direct Verification Link:")
    print(f"{Fore.WHITE}  ➤ {LINK} (Password: {PASS})")
    print(f"\n{Fore.GREEN}================ SCAN COMPLETE ================")

if __name__ == "__main__":
    main()
