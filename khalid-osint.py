import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Config
P_URL = "https://anishexploits.site/app/"
ACCESS_KEY = "Anish123"

def run_portal_priority(target, report_file):
    """Bina kisi heading ke direct portal data dikhayega"""
    try:
        payload = {'access_key': ACCESS_KEY, 'number': target, 'submit': 'CHECK NOW'}
        response = requests.post(P_URL, data=payload, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            labels = ["Number :", "Name :", "Father :", "Address :", "Circle :", "Aadhar :"]
            
            print(f"\n{Fore.GREEN}--- [ PORTAL RESULTS ] ---")
            with open(report_file, "a") as f:
                # Scrape only relevant identity lines
                for tag in soup.find_all(['li', 'p', 'div', 'span']):
                    text = tag.get_text().strip()
                    if any(label in text for label in labels):
                        print(f"{Fore.WHITE}{text}")
                        f.write(f"{text}\n")
            print(f"{Fore.GREEN}--------------------------\n")
    except:
        print(f"{Fore.RED}[!] Portal connection failed.")

def run_background_tools(cmd, name, report_file):
    """Saare tools bina kisi error ke kaam karenge"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "link:"]):
                    print(f"{Fore.CYAN}[+] {name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{name}: {line.strip()}\n")
    except:
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.YELLOW}KHALID MASTER OSINT - (PORTAL FIRST MODE)")
    
    target = input(f"\n[?] Enter Target (Phone/User): ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # Priority #1: Anish Portal
    run_portal_priority(target, report_path)
    
    # Full Toolset (No tools removed)
    print(f"{Fore.BLUE}[*] Checking secondary databases for {target}...")
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer")
    ]
    
    for cmd, name in tools:
        run_background_tools(cmd, name, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] All Results Saved. Report Path: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
