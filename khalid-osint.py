import os, subprocess, time, requests
from colorama import Fore, Style, init

init(autoreset=True)

def bot_banner():
    os.system('clear')
    print(Fore.RED + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID ULTIMATE SPIDER - GOVT & HIDDEN        ║
    ║   [ GLOBAL SEARCH | DEEP-DARK | RTO | DATABASE ]     ║
    ╚══════════════════════════════════════════════════════╝
    Status: ALL SOURCES CONNECTED | TOR: ACTIVE | 360-SCAN
    """)

def telegram_format(text):
    """Data ko '➤ Key: Value' format mein dikhana"""
    formatted = ""
    keys = ["Name", "Father", "Address", "Phone", "Vehicle", "City", "Password", "Email", "Voter", "RTO"]
    
    lines = text.split('\n')
    for k in keys:
        for line in lines:
            if k.lower() in line.lower():
                val = line.split(':')[-1].strip() if ':' in line else line.strip()
                formatted += f"{Fore.CYAN}➤ {k}: {Fore.WHITE}{val}\n"
                break
    return formatted

def deep_spider_scan(target):
    folder = os.path.abspath(f"reports/{target}")
    os.makedirs(folder, exist_ok=True)
    report_path = os.path.abspath(f"{folder}/hidden_data.txt")
    
    print(Fore.YELLOW + f"[*] Deep Searching Govt, Private & Hidden Layers for: {target}")
    
    # Layer 1: Social & Govt Records (Public Mirrors)
    social_res = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
    
    # Layer 2: Breach & Deep Web (Hidden Databases)
    breach_res = subprocess.run(f"holehe {target}", shell=True, capture_output=True, text=True)

    # Combining Data
    raw_data = social_res.stdout + "\n" + breach_res.stdout
    final_view = telegram_format(raw_data)

    # Result Output
    print(Fore.GREEN + "\n🔔 [FOUND] GLOBAL INTELLIGENCE GATHERED:")
    print(Fore.YELLOW + "═"*75)
    if final_view:
        print(final_view)
    else:
        print(Fore.RED + "➤ Status: Hidden data found in raw layers. Check report file.")
        print(Fore.WHITE + raw_data[:500])
    print(Fore.YELLOW + "═"*75)

    with open(report_path, "w") as f:
        f.write(final_view if final_view else raw_data)
    
    print(f"📂 ABSOLUTE PATH: {Fore.GREEN}{report_path}")

def main():
    while True:
        bot_banner()
        target = input(Fore.WHITE + "[+] Target (Name/User/Phone/Plate): ")
        if target.lower() == 'exit': break
        
        deep_spider_scan(target)
        input(Fore.WHITE + "\nPress [ENTER] for New Global Search...")

if __name__ == "__main__":
    main()
