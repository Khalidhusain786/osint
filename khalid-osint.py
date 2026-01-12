import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

P_URL = "https://anishexploits.site/app/"

def stream_found_only(cmd, tool_name, target):
    """Terminal par kachra saaf karke sirf results dikhana"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Filter logic for found data only
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:", "name:", "address:"]):
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{tool_name}: {line}\n")
    except: pass

def check_portal(target):
    """Anish Portal se HTML kachra saaf karke data nikalna"""
    print(f"\n{Fore.CYAN}[*] Check Now: Fetching Records for {target}...")
    try:
        resp = requests.post(P_URL, data={'number': target}, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            clean_text = soup.get_text(separator="\n").strip()
            # Kaam ki fields filter karna
            keys = ["Name", "Father", "Address", "Circle", "Aadhar", "Number :"]
            found = [l.strip() for l in clean_text.split('\n') if any(k in l for k in keys)]
            
            if found:
                print(f"{Fore.GREEN}--- [ REAL DATA FOUND ] ---")
                for item in found: print(f"{Fore.WHITE}{item}")
                print(f"{Fore.GREEN}---------------------------")
                with open(f"reports/{target}.txt", "a") as f: f.write("\n".join(found) + "\n")
    except: print(f"{Fore.RED}[!] Portal offline.")

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - (30+ TOOLS & NO-ERROR MODE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    
    # 1. Clean Portal Check
    check_portal(target)
    
    # 2. Scanning with All Tools (Including Social Analyzer)
    print(f"\n{Fore.BLUE}[*] Scanning All Databases... (Found-Only Mode)\n")
    
    tools = [
        (f"phoneinfoga scan -n {target}", "Phone-Info"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"holehe {target} --only-used", "Holehe-Email"),
        (f"maigret {target} --timeout 10", "Maigret-Identity"),
        (f"blackbird -u {target}", "Blackbird"),
        (f"ignorant {target}", "Ignorant-Gmail")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target)
        
    print(f"\n{Fore.YELLOW}[➔] Scan Complete. Report saved in reports/{target}.txt")

if __name__ == "__main__":
    main()
