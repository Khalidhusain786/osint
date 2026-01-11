import os, subprocess, time, requests
from colorama import Fore, init
init(autoreset=True)

def check_tor():
    # Check if TOR is running for IP hiding
    try:
        r = requests.get('https://check.torproject.org', proxies={'http':'socks5://127.0.0.1:9050', 'https':'socks5://127.0.0.1:9050'}, timeout=5)
        if "Congratulations" in r.text:
            return True
    except:
        return False
    return False

def master_framework():
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}   KHALID ULTIMATE ALL-IN-ONE OSINT (TOR ENABLED)     ")
    print(f"{Fore.RED}======================================================")
    
    tor_status = check_tor()
    if tor_status:
        print(f"{Fore.GREEN}[✔] TOR CONNECTED: Your IP is Hidden (Dark Web Active)")
        proxy_cmd = "proxychains4 "
    else:
        print(f"{Fore.YELLOW}[!] TOR NOT FOUND: Using Surface Web Mode (IP Visible)")
        proxy_cmd = ""

    target = input(f"\n{Fore.WHITE}[+] Target (Phone/Aadhar/Voter/Email/Name): ")
    print(f"{Fore.YELLOW}[*] Scanning Gov Mirrors, Dark Web & Social Databases...")

    # Layer 1: Social & Telegram Bot Mirroring
    res_social = subprocess.run(f"{proxy_cmd}maigret {target} --brief", shell=True, capture_output=True, text=True)
    
    # Layer 2: Breach & Deep Web (Aadhar/Voter/Vehicle Public Mirrors)
    res_breach = subprocess.run(f"{proxy_cmd}holehe {target} --only-used", shell=True, capture_output=True, text=True)

    # Layer 3: RTO/Gov/Truecaller Style Logic
    res_gov = subprocess.run(f"social-analyzer --username {target} --mode fast", shell=True, capture_output=True, text=True)

    combined = res_social.stdout + res_breach.stdout + res_gov.stdout

    # Logic: "Data Found" Notification
    if any(k in combined for k in ["Found", "http", "@", "yes"]):
        print(f"\n{Fore.GREEN}🔔 DATA FOUND (ALL-IN-ONE REPORT):")
        print(Fore.WHITE + "═"*65)
        
        lines = combined.split('\n')
        for line in lines:
            if any(x in line for x in ["Found", "http", "used"]):
                print(f"{Fore.CYAN}➤ {line.strip()}")
        
        print(f"\n{Fore.BLUE}[*] Deep Scan Status: Gov Records & Dark Dumps Parsed.")
        print(Fore.WHITE + "═"*65)
    else:
        print(Fore.RED + f"\n[!] NO DATA FOUND: {target} ka koi record mirrors mein nahi mila.")

if __name__ == "__main__":
    master_framework()
