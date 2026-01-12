import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

# Portal Configuration
P_URL = "https://anishexploits.site/app/"
ACCESS_KEY = "Anish123"

def run_portal_first(target, report_file):
    """Sabse pehle portal ka data dikhayega"""
    try:
        payload = {'access_key': ACCESS_KEY, 'number': target, 'submit': 'CHECK NOW'}
        response = requests.post(P_URL, data=payload, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Scrape specific labels
            labels = ["Number :", "Name :", "Father :", "Address :", "Circle :", "Aadhar :"]
            
            print(f"\n{Fore.GREEN}--- [ PORTAL RESULTS ] ---")
            found = False
            with open(report_file, "a") as f:
                for tag in soup.find_all(['li', 'p', 'div', 'span']):
                    text = tag.get_text().strip()
                    if any(label in text for label in labels):
                        print(f"{Fore.WHITE}{text}")
                        f.write(f"{text}\n")
                        found = True
            
            if not found:
                # Agar formatted data na mile toh pura text dikhao
                clean_text = soup.get_text(separator="\n").strip()
                for line in clean_text.split("\n"):
                    if any(l in line for l in labels):
                        print(f"{Fore.WHITE}{line.strip()}")
            print(f"{Fore.GREEN}--------------------------\n")
    except:
        print(f"{Fore.RED}[!] Portal offline or Connection failed.")

def run_other_tools(cmd, name, report_file):
    """Baaki tools backup mein chalenge"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "link:"]):
                    print(f"{Fore.CYAN}[+] {name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{name}: {line.strip()}\n")
