import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Config
P_URL = "https://anishexploits.site/app/"

def stream_found_only(cmd, tool_name, target, report_file):
    """Terminal par errors filter karke sirf results dikhana"""
    try:
        # Errors (stderr) ko dev/null mein bhej rahe hain taaki screen saaf rahe
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Sirf Links aur positive matches show honge
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line.strip()}\n")
    except: pass

def portal_check(target, report_file):
    """Anish Portal se clean data nikalna"""
    print(f"\n{Fore.CYAN}[*] Searching Private Database Records...")
    try:
        resp = requests.post(P_URL, data={'number': target}, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            clean_text = soup.get_text(separator="\n").strip()
            keys = ["Name", "Father", "Address", "Circle", "Aadhar", "Number :"]
            found = [l.strip() for l in clean_text.split('\n') if any(k in l for k in keys)]
            if found:
                print(f"{Fore.GREEN}--- [ REAL DATA FOUND ] ---")
                for item in found: print(f"{Fore.WHITE}{item}")
                with open(report_file, "a") as f: f.write("\n".join(found) + "\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (ZERO-ERROR SYSTEM)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # 1. Clean Portal Check
    portal_check(target, report_path)
    
    # 2. Global Scan (Saare tools linked hain)
    print(f"\n{Fore.BLUE}[*] Scanning All 30+ Modules... (Found-Only Mode)\n")
    
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer"),
        (f"holehe {target} --only-used", "Holehe-Email"),
        (f"maigret {target} --timeout 10", "Maigret-Identity"),
        (f"blackbird -u {target}", "Social-Blackbird")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Completed! Notepad band rakha gaya hai.")
    print(f"{Fore.CYAN}[REPORT SAVED AT]: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
