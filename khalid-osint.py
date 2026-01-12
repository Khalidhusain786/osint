import os, subprocess, requests
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Configuration
P_URL = "https://anishexploits.site/app/"
ACCESS_KEY = "Anish123"

def run_auto_portal(target):
    """Website automatically open hogi aur data extract karegi"""
    try:
        print(f"{Fore.YELLOW}[*] Connecting to Anish Portal with Auto-Login...")
        payload = {'access_key': ACCESS_KEY, 'number': target, 'submit': 'CHECK NOW'}
        response = requests.post(P_URL, data=payload, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extracting Name, Father, Address from the portal
            labels = ["Number :", "Name :", "Father :", "Address :", "Circle :", "Aadhar :"]
            
            print(f"\n{Fore.GREEN}--- [ PORTAL FOUND DATA ] ---")
            found = False
            for tag in soup.find_all(['li', 'p', 'div', 'span']):
                text = tag.get_text().strip()
                if any(label in text for label in labels):
                    print(f"{Fore.WHITE}{text}")
                    found = True
            
            if not found:
                print(f"{Fore.RED}[!] Website opened but no data found for this number.")
            print(f"{Fore.GREEN}-----------------------------\n")
    except Exception as e:
        print(f"{Fore.RED}[!] Connection Error: {str(e)}")

def run_other_tools(cmd, name):
    """Running Sherlock, Holehe, etc."""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        for line in process.stdout:
            if any(x in line.lower() for x in ["http", "found", "[+]"]):
                print(f"{Fore.CYAN}[+] {name}: {Fore.WHITE}{line.strip()}")
    except:
        pass

def main():
    os.system('clear')
    print(f"{Fore.RED}KHALID MASTER OSINT - AUTO PORTAL MODE")
    target = input(f"\n{Fore.YELLOW}[?] Enter Target Number: ")
    
    # Step 1: Portal Auto-Login & Extraction
    run_auto_portal(target)
    
    # Step 2: All Other Tools (No deletion)
    print(f"{Fore.BLUE}[*] Running 30+ Secondary OSINT Tools...\n")
    tools = [
        (f"sherlock {target} --timeout 1", "Sherlock"),
        (f"holehe {target}", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"phoneinfoga scan -n {target}", "PhoneInfo")
    ]
    
    for cmd, name in tools:
        run_other_tools(cmd, name)

if __name__ == "__main__":
    main()
