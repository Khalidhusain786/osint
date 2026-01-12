import os, subprocess, requests
from colorama import Fore, init

init(autoreset=True)

# Portal Configuration (Fully Hidden)
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123" 

def silent_portal_unlock():
    """Background mein portal unlock karega bina password dikhaye"""
    try:
        session = requests.Session()
        # Password auto-inject logic
        response = session.post(P_URL, data={'password': P_KEY}, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[✔] PORTAL ACCESS GRANTED")
            return session
    except:
        pass
    return None

def run_engine(cmd, name):
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        # Filtering: Sirf real social/email links dikhayega
        out = [l.strip() for l in (proc.stdout + proc.stderr).split('\n') if "http" in l.lower() and "404" not in l]
        if out:
            print(f"{Fore.GREEN}\n[+] {name.upper()} DATA FOUND:")
            for link in out[:10]:
                print(f"{Fore.WHITE}  ➤ {link}")
    except: pass

def main():
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}           KHALID PRIVATE OSINT FRAMEWORK             ")
    print(f"{Fore.RED}======================================================")
    
    # Hidden Auto-Login
    session = silent_portal_unlock()
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Username/Email): ")
    print(f"{Fore.CYAN}[*] Searching Securely... (Waiting for Data)\n")

    # Core Engines (Sirf Found data hi screen par aayega)
    run_engine(f"sherlock {target} --timeout 1 --print-found", "Social Media")
    run_engine(f"holehe {target} --only-used", "Email Leak")

    print(f"\n{Fore.CYAN}================ SCAN FINISHED ================")

if __name__ == "__main__":
    main()
