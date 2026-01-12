import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# New Portal Config (As per Screenshot 07_58_51)
P_URL = "https://anishexploits.site/app/"

def stream_found_only(cmd, tool_name, target):
    """Sirf found results terminal par chamkenge"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line}\n")
    except: pass

def check_now_portal(target):
    """Naye portal se seedha data fetch karna"""
    print(f"\n{Fore.CYAN}[*] Check Now: Fetching from Private Database...")
    try:
        # Direct number submission logic
        resp = requests.post(P_URL, data={'number': target}, timeout=15)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Sirf kaam ka data nikalna (Icons aur details)
            clean_text = soup.get_text(separator="\n").strip()
            
            # Filtering out menu/generic text
            lines = [l.strip() for l in clean_text.split('\n') if len(l.strip()) > 3 and "CHECK NOW" not in l and "Recording" not in l]
            final_data = "\n".join(lines)

            if len(final_data) > 10:
                print(f"{Fore.GREEN}--- [ REAL DATA FOUND ] ---")
                print(Fore.WHITE + final_data)
                print(f"{Fore.GREEN}---------------------------")
                with open(f"reports/{target}.txt", "a") as f:
                    f.write(f"\n--- PORTAL DATA ---\n{final_data}\n")
            else:
                print(f"{Fore.RED}[!] No data found for this number.")
    except:
        print(f"{Fore.RED}[!] Portal server busy or offline.")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (NEW PORTAL BYPASS)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    report_path = f"reports/{target}.txt"
    
    # 1. New Portal Check Now Logic
    check_now_portal(target)
    
    # 2. Tools Execution (Sirf Found Results)
    print(f"\n{Fore.BLUE}[*] Scanning Global Profiles... (Found-Only)\n")
    tools = [
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Opening Report...")
    os.system(f"mousepad {report_path} &")
