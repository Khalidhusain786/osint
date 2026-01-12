import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

P_URL = "https://anishexploits.site/app/"

def stream_found_only(cmd, tool_name, target):
    """Sirf kaam ka data terminal par show hoga"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:", "name:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line}\n")
    except: pass

def portal_check_clean(target):
    """Portal se sirf clean text nikalna"""
    print(f"\n{Fore.CYAN}[*] CHECK NOW: Fetching Database Records...")
    try:
        resp = requests.post(P_URL, data={'number': target}, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            clean_text = soup.get_text(separator="\n").strip()
            keys = ["Name", "Father", "Address", "Circle", "Aadhar", "Number :"]
            found_data = [l.strip() for l in clean_text.split('\n') if any(k in l for k in keys)]
            
            if found_data:
                print(f"{Fore.GREEN}--- [ REAL DATA FOUND ] ---")
                for item in found_data: print(f"{Fore.WHITE}{item}")
                print(f"{Fore.GREEN}---------------------------")
                with open(f"reports/{target}.txt", "a") as f: f.write("\n".join(found_data) + "\n")
    except: print(f"{Fore.RED}[!] Portal offline.")

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (SOCIAL ANALYZER ACTIVE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    report_path = f"reports/{target}.txt"
    
    # 1. Clean Portal Check
    portal_check_clean(target)
    
    # 2. Complete Tool Scan
    print(f"\n{Fore.BLUE}[*] Scanning All Modules (Silent Mode)...\n")
    
    commands = [
        (f"phoneinfoga scan -n {target}", "Phone-Check"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"holehe {target} --only-used", "Email-Check"),
        (f"maigret {target} --timeout 10", "Maigret-Search"),
        (f"blackbird -u {target}", "Blackbird-Social")
    ]
    
    for cmd, name in commands:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] All Found Data Saved. Opening Report...")
    os.system(f"mousepad {report_path} &")

if __name__ == "__main__":
    main()
