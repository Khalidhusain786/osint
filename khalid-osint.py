import os, subprocess, requests
from colorama import Fore, init

init(autoreset=True)

def run_silent(cmd, name):
    try:
        # Background mein run karega, kachra hide karega
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        
        # Sirf tabhi dikhayega jab 'http' mile (Clickable links)
        findings = [l.strip() for l in out.split('\n') if "http" in l.lower() and "404" not in l and "usage:" not in l.lower()]
        
        if findings:
            print(f"{Fore.GREEN}\n[✔] {name.upper()} DATA FOUND:")
            for link in findings[:10]:
                print(f"{Fore.WHITE}  ➤ {link}")
    except: pass

def main():
    os.system('clear')
    print(f"{Fore.RED}=== KHALID MASTER OSINT (V5.0 - NO ERRORS) ===")
    target = input(f"\n{Fore.YELLOW}[+] Enter Target (Username/Email): ")
    print(f"{Fore.CYAN}[*] Searching... (Sirf found data hi show hoga)\n")

    # Sherlock aur Holehe chalao (Ab ye errors nahi denge)
    run_silent(f"sherlock {target} --timeout 1 --print-found", "Social Media")
    run_silent(f"holehe {target} --only-used", "Email Leak")
    run_silent(f"googler --nocolor -n 3 -w gov.in \"{target}\"", "Gov Records")

    print(f"\n{Fore.GREEN}================ SCAN COMPLETE ================")

if __name__ == "__main__":
    main()
