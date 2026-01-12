import os, subprocess, requests
from colorama import Fore, init

init(autoreset=True)

def run_check(cmd, name):
    """Check karna ki tool install hai ya nahi"""
    try:
        proc = subprocess.run(f"which {cmd}", shell=True, capture_output=True, text=True)
        return proc.returncode == 0
    except: return False

def search_engine(cmd, name, target):
    """Sirf Found results dikhane ke liye"""
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        
        # Filtering for links and successful hits
        findings = [l.strip() for l in out.split('\n') if "http" in l.lower() and "404" not in l and "usage:" not in l.lower()]
        
        if findings:
            print(f"{Fore.GREEN}\n[✔] {name.upper()} DATA FOUND:")
            for link in findings[:10]:
                print(f"{Fore.WHITE}  ➤ {link}")
    except: pass

def main():
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID ULTIMATE OSINT - NO ERROR MODE          ")
    print(f"{Fore.RED}======================================================")
    
    target = input(f"\n{Fore.YELLOW}[+] Enter Target (User/Email/Phone): ")
    print(f"{Fore.CYAN}[*] Scannning... (Faltu errors hide kar diye gaye hain)\n")

    # 1. Social Scan (Sherlock)
    if run_check("sherlock", "Sherlock"):
        search_engine(f"sherlock {target} --timeout 1 --print-found", "Social-Accounts", target)
    
    # 2. Email Scan (Holehe)
    if run_check("holehe", "Holehe"):
        search_engine(f"holehe {target} --only-used", "Email-Check", target)

    # 3. Web Scan (Googler)
    if run_check("googler", "Googler"):
        search_engine(f"googler --nocolor -n 3 -w gov.in \"{target}\"", "Gov-Records", target)

    # 4. Manual Verification Links
    print(f"{Fore.BLUE}\n[*] Direct Clickable Verification Links:")
    check_urls = [f"https://www.instagram.com/{target}", f"https://github.com/{target}"]
    for url in check_urls:
        print(f"{Fore.WHITE}  ➤ {url}")

    print(f"\n{Fore.GREEN}================ SCAN FINISHED ================")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    main()
