import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Sirf found links terminal par chamkenge"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Filter logic: Sirf valid hits
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line}\n")
    except: pass

def check_now_portal(target):
    """Key auto-submit karke HTML kachra saaf karke dikhana"""
    print(f"\n{Fore.CYAN}[*] Check Now: Accessing Private Database...")
    try:
        session = requests.Session()
        # Access Key 'Anish123' auto-submit logic
        resp = session.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Removing HTML tags for clean text
            clean_text = soup.get_text(separator="\n").strip()
            
            # Filtering out generic website text
            lines = [l.strip() for l in clean_text.split('\n') if len(l.strip()) > 2 and "Submit" not in l and "Access Key" not in l]
            final_data = "\n".join(lines)

            if len(final_data) > 10:
                print(f"{Fore.GREEN}--- [ FOUND DATA ] ---")
                print(Fore.WHITE + final_data)
                print(f"{Fore.GREEN}----------------------")
                with open(f"reports/{target}.txt", "a") as f:
                    f.write(f"\n--- CLEAN PORTAL DATA ---\n{final_data}\n")
    except:
        print(f"{Fore.RED}[!] Portal connection failed.")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (PURE FOUND MODE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    report_path = f"reports/{target}.txt"
    
    # 1. Background Portal Check (Clean Text)
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
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Opening Clean Report...")
    # Report auto-open in Mousepad
    os.system(f"mousepad {report_path} &")
