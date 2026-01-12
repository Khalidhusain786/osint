import os, subprocess, requests, sys
from colorama import Fore, init
from bs4 import BeautifulSoup

init(autoreset=True)

P_URL = "https://anishexploits.site/app/"

def stream_found_only(cmd, tool_name, target, report_file):
    """Sirf Found results aur Links dikhayega"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Sirf positive matches filter honge
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    clean_line = line.strip()
                    print(f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{clean_line}")
                    f.write(f"{tool_name}: {clean_line}\n")
    except: pass

def check_portal(target, report_file):
    """Portal se clean data (Aadhar/Name) nikalna"""
    print(f"\n{Fore.CYAN}[*] Fetching Portal Records...")
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
    print(f"{Fore.RED}KHALID MASTER OSINT - (STRICT FOUND-ONLY MODE)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # 1. Portal Check
    check_portal(target, report_path)
    
    # 2. Global Scan (Silent Mode)
    print(f"\n{Fore.BLUE}[*] Scanning All Linked Tools... (Found-Only)\n")
    
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"blackbird -u {target}", "SocialSearch")
    ]
    
    for cmd, name in tools:
        stream_found_only(cmd, name, target, report_path)
        
    # Notepad nahi khulega, sirf path dikhayega
    print(f"\n{Fore.YELLOW}[➔] Scan Complete!")
    print(f"{Fore.CYAN}[FILE SAVED AT]: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
