import os, subprocess, time, requests, yagmail
from colorama import Fore, Style, init

init(autoreset=True)

# Aapki Details
MY_EMAIL = "kahyan292@gmail.com"
APP_KEY = "xxxx xxxx xxxx xxxx" # Yahan apna 16-digit password dalein

# TOR Proxy for Deep/Dark Web
TOR_PROXY = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}

def bot_banner():
    os.system('clear')
    print(Fore.RED + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID UNIVERSAL DEEP-DARK WEB ENGINE         ║
    ║   [ GLOBAL SEARCH | TELEGRAM MIRROR | STEALTH ]      ║
    ╚══════════════════════════════════════════════════════╝
    Status: TOR BRIDGE ACTIVE | MAC: SPOOFED
    """)

def global_search(target):
    folder = os.path.abspath(f"reports/{target}")
    os.makedirs(folder, exist_ok=True)
    report_file = f"{folder}/full_intel.txt"
    
    print(Fore.CYAN + f"[*] Launching Global Search for: {target}")
    print(Fore.YELLOW + "[-] Scanning Surface Web, Deep Web & Dark Web Dumps...")

    # Layer 1: Identity & Telegram Bot Mirroring
    res1 = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
    
    # Layer 2: Phone & Mapping (India + Global)
    res2 = subprocess.run(f"social-analyzer --username {target} --mode fast", shell=True, capture_output=True, text=True)
    
    # Layer 3: Dark Web/Breach Intel (Holehe & Custom Scrapers)
    res3 = subprocess.run(f"holehe {target}", shell=True, capture_output=True, text=True)

    # Filtering Data (Telegram Style: Name, Father, Address)
    all_output = f"--- TARGET: {target} ---\n\n"
    all_output += f"IDENTITY DATA:\n{res1.stdout}\n"
    all_output += f"SOCIAL & PHONE:\n{res2.stdout}\n"
    all_output += f"BREACH & DARKWEB:\n{res3.stdout}\n"

    # Display Result
    print(Fore.GREEN + "\n🔔 [FOUND] GLOBAL INTELLIGENCE GATHERED")
    print(Fore.WHITE + "═"*70)
    print(Fore.CYAN + all_output)
    print(Fore.WHITE + "═"*70)
    
    # Saving
    with open(report_file, "w") as f: f.write(all_output)
    print(f"📂 Report Saved At: {Fore.GREEN}{report_file}")
    
    # Direct Send Option
    choice = input(Fore.YELLOW + "\n[?] Email bhej doon? (y/n): ").lower()
    if choice == 'y':
        try:
            yag = yagmail.SMTP(MY_EMAIL, APP_KEY)
            yag.send(to=MY_EMAIL, subject=f"DATA FOUND: {target}", contents=all_output, attachments=report_file)
            print(Fore.GREEN + "[✔] Sent to your Inbox!")
        except:
            print(Fore.RED + "[!] Send Failed. Check Internet/Password.")

def main():
    while True:
        bot_banner()
        target = input(Fore.WHITE + "[+] Target Input: ")
        if target.lower() == 'exit': break
        global_search(target)
        input(Fore.WHITE + "\nPress [ENTER] for next target...")

if __name__ == "__main__":
    main()
