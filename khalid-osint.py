import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Latest Portal Link
P_URL = "https://anishexploits.site/app/"

def stream_found_only(cmd, tool_name, target):
    """Sirf found results terminal par dikhayega"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line}\n")
    except: pass

def check_now_clean(target):
    """Portal se sirf real data nikalna"""
    print(f"\n{Fore.CYAN}[*] Check Now: Fetching Clean Data...")
    try:
        resp = requests.post(P_URL, data={'number': target}, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Sirf text nikalna
            clean_text = soup.get_text(separator="\n").strip()
            
            # Sirf wahi lines dikhana jismein kaam ki info ho
            important_keywords = ["Name", "Father", "Address", "Circle", "Number :", "Aadhar"]
            found_lines = []
            
            for line in clean_text.split('\n'):
                if any(key in line for key in important_keywords):
                    found_lines.append(line.strip())

            if found_lines:
                print(f"{Fore.GREEN}--- [ FOUND DATA ] ---")
                for info in found_lines:
                    print(f"{Fore.WHITE}{info}")
                print(f"{Fore.GREEN}----------------------")
                with open(f"reports/{target}.txt", "a") as f:
                    f.write("\n".join(found_lines))
            else:
                print(f"{Fore.RED}[!] No clean data found.")
    except:
        print(f"{Fore.RED}[!] Connection error.")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (FINAL PATH & DATA FIX)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    report_path = f"reports/{target}.txt"
    
    # 1. Clean Portal Data Fetch
    check_now_clean(target)
    
    # 2. Global Tools (Only Found)
    print(f"\n{Fore.BLUE}[*] Scanning Online Profiles... (Sirf 'Found' data)\n")
    tools = [
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Opening Clean Report...")
    os.system(f"mousepad {report_path} &")
