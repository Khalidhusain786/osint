import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

P_URL = "https://anishexploits.site/app/"

def stream_found_only(cmd, tool_name, target, report_file):
    """Sirf found links show honge"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line.strip()}\n")
    except: pass

def portal_check(target, report_file):
    """Anish Portal clean data extraction"""
    print(f"\n{Fore.CYAN}[*] Searching Private Database Records...")
    try:
        resp = requests.post(P_URL, data={'number': target}, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            clean_text = soup.get_text(separator="\n").strip()
            keys = ["Name", "Father", "Address", "Circle", "Aadhar", "Number :"]
            found = [l.strip() for l in clean_text.split('\n') if any(k in l for k in keys)]
            if found:
                print(f"{Fore.GREEN}--- [ FOUND DATA ] ---")
                for item in found: print(f"{Fore.WHITE}{item}")
                with open(report_file, "a") as f: f.write("\n".join(found) + "\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (ALL TOOLS INTEGRATED)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # 1. Portal Data
    portal_check(target, report_path)
    
    # 2. Scanning with All Modules (Missing tools added here)
    print(f"\n{Fore.BLUE}[*] Scanning All Databases... (Found-Only Mode)\n")
    
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"blackbird -u {target}", "Blackbird"),
        (f"photon -u {target}", "Photon-Recon")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Finished! Notepad won't open automatically.")
    print(f"{Fore.CYAN}[FILE PATH]: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
