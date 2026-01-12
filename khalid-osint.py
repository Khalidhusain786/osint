import os, time, requests, subprocess
from colorama import Fore, init
from telethon.sync import TelegramClient

init(autoreset=True)

# --- APNI DETAILS YAHAN BHAREIN ---
API_ID = 'Aapka_API_ID' 
API_HASH = 'Aapka_API_HASH'
# Screenshot wale aur extra bots
BOT_LIST = [
    'osint_bot_link', 
    'breacheddatabot', 
    'HiTeck_Checker_bot', 
    'Hiddnosint_bot'
]

def telegram_deep_scan(target):
    print(f"{Fore.MAGENTA}[*] Mirroring Telegram Databases (Deep Scan)...")
    try:
        with TelegramClient('khalid_session', API_ID, API_HASH) as client:
            for bot in BOT_LIST:
                print(f"{Fore.CYAN}[>] Sending query to @{bot}...")
                client.send_message(bot, target)
                time.sleep(5) # Bot reply ke liye wait
                
                # Bot ka last reply read karein
                messages = client.get_messages(bot, limit=1)
                for msg in messages:
                    if msg.text and any(k in msg.text.lower() for k in ["name", "address", "phone", "father", "document"]):
                        print(f"{Fore.GREEN}\n[✔] DATA FOUND FROM @{bot}:")
                        print(f"{Fore.WHITE}{msg.text}")
                        # Save to report
                        with open(f"reports/{target}_telegram.txt", "a") as f:
                            f.write(f"\nSource: @{bot}\n{msg.text}\n{'-'*30}")
                    else:
                        print(f"{Fore.RED}[-] No direct hits in @{bot}")
    except Exception as e:
        print(f"{Fore.RED}[!] Telegram Error: {e}")

def master():
    os.system('clear')
    print(f"{Fore.RED}=== KHALID DEEP-SEARCH OSINT (TELEGRAM MIRROR) ===")
    
    target = input(f"\n{Fore.YELLOW}[+] Enter Target (Phone/Name/Email): ")
    
    # Layer 1: Normal Tools (Optional)
    # subprocess.run(f"maigret {target} --brief", shell=True)
    
    # Layer 2: Telegram Bots (Screenshot Logic)
    telegram_deep_scan(target)
    
    print(f"\n{Fore.GREEN}[!] All data saved in reports/{target}_telegram.txt")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    master()
