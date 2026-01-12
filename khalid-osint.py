import os, subprocess, requests, time
from colorama import Fore, init
from telethon.sync import TelegramClient

init(autoreset=True)

# --- APNI DETAILS YAHAN BHAREIN (ONLY ONCE) ---
API_ID = 'YOUR_API_ID' 
API_HASH = 'YOUR_API_HASH'
# Screenshot wale bots ki list
BOTS = ['osint_bot_link', 'breacheddatabot', 'HiTeck_Checker_bot', 'Hiddnosint_bot']

def check_tor():
    try:
        r = requests.get('https://check.torproject.org', proxies={'http':'socks5://127.0.0.1:9050', 'https':'socks5://127.0.0.1:9050'}, timeout=5)
        return "Congratulations" in r.text
    except: return False

def telegram_mirror_scan(target):
    print(f"{Fore.MAGENTA}[*] Deep Searching Telegram Bot Databases...")
    try:
        with TelegramClient('khalid_session', API_ID, API_HASH) as client:
            for bot in BOTS:
                client.send_message(bot, target)
                time.sleep(5) # Bot reply wait
                msgs = client.get_messages(bot, limit=1)
                for m in msgs:
                    if m.text and any(k in m.text.lower() for k in ["name", "father", "address", "phone"]):
                        print(f"{Fore.GREEN}\n[✔] DATA FOUND IN @{bot}:")
                        print(f"{Fore.WHITE}{m.text}")
                        with open(f"reports/{target}_data.txt", "a") as f:
                            f.write(f"\n--- From @{bot} ---\n{m.text}\n")
    except Exception as e: print(f"{Fore.RED}[!] Telegram Error: {e}")

def main_run():
    os.system('clear')
    print(f"{Fore.RED}KHALID ULTIMATE OSINT FRAMEWORK (v3.0)")
    
    tor = check_tor()
    proxy = "proxychains4 " if tor else ""
    target = input(f"\n{Fore.YELLOW}[+] Enter Target (Phone/User/Email): ")
    
    # 1. Social Layer
    print(f"{Fore.CYAN}[*] Searching Social Media...")
    subprocess.run(f"{proxy}maigret {target} --brief", shell=True)
    
    # 2. Telegram Database Layer (Screenshot Logic)
    telegram_mirror_scan(target)
    
    print(f"\n{Fore.GREEN}Scan Complete! Full Report: reports/{target}_data.txt")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    main_run()
