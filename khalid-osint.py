import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Config (Auto-Submit Key)
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def stream_found_only(cmd, tool_name, target):
    """Sirf found results terminal par dikhayega"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Filter logic: Sirf valid hits terminal par show honge
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    clean = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean}")
                    f.write(f"{tool_name}: {clean}\n")
    except: pass

def auto_check_portal(target):
    """Anish123 key auto-submit karke clean data dikhana"""
    print(f"\n{Fore.CYAN}[*] Check Now: Accessing Private Database...")
    try:
        session = requests.Session()
        # Auto-submitting the access key
        resp = session.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # HTML tags ko hatakar sirf saaf data nikalna
            clean_text = soup.get_text(separator="\n").strip()
            
            if len(clean_text) > 5:
                print(f"{Fore.GREEN}--- [ FOUND DATA ] ---")
                print(Fore.WHITE + clean_text)
                print(f"{Fore.GREEN}----------------------")
                with open(f"reports/{target}.txt", "a") as f:
                    f.write(f"\n--- PORTAL DATA ---\n{clean_text}\n")
    except:
        print(f"{Fore.RED}[!] Portal access failed.")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (AUTO-KEY & FOUND-ONLY)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    report_path = f"reports/{target}.txt"
    
    # 1. Anish Portal Auto-Check
    auto_check_portal(target)
    
    # 2. Global Scan (Silent Mode)
    print(f"\n{Fore.BLUE}[*] Checking Global Tools... (Sirf 'Found' results)\n")
    tools = [
        (f"phoneinfoga scan -n {target}", "Phone-Info"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe Email"),
        (f"maigret {target} --timeout 10", "Identity")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Report opening in Notepad...")
    # Scan ke baad report auto-open
    os.system(f"mousepad {report_path} &")
