import os, subprocess, requests, time
from colorama import Fore, init
from telethon.sync import TelegramClient

init(autoreset=True)

# --- CONFIGURATION (Sirf Ek Baar Karein) ---
API_ID = 'YOUR_API_ID' 
API_HASH = 'YOUR_API_HASH'
TELEGRAM_BOTS = ['osint_bot_link', 'breacheddatabot', 'HiTeck_Checker_bot', 'Hiddnosint_bot', 'Ryd_osintbot']

def check_tor():
    try:
        r = requests.get('https://check.torproject.org', proxies={'http':'socks5://127.0.0.1:9050', 'https':'socks5://127.0.0.1:9050'}, timeout=5)
        return "Congratulations" in r.text
    except: return False

def log_data(name, data, target):
    if data.strip():
        print(f"{Fore.GREEN}\n[✔] {name.upper()} SE DATA MIL GAYA:")
        print(f"{Fore.WHITE}{data}")
        with open(f"reports/{target}_master_report.txt", "a") as f:
            f.write(f"\n--- {name} ---\n{data}\n")

def run_tool(cmd, name, target):
    print(f"{Fore.CYAN}[*] {name} Scan Chal Raha Hai...")
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    found = "\n".join([l for l in out.split('\n') if any(k in l.lower() for k in ["found", "http", "address", "father", "user"]) and "404" not in l])
    log_data(name, found, target)

def telegram_scan(target):
    print(f"{Fore.MAGENTA}[*] Telegram Bots Se Deep Search Kar Raha Hoon...")
    try:
        with TelegramClient('khalid_session', API_ID, API_HASH) as client:
            for bot in TELEGRAM_BOTS:
                client.send_message(bot, target)
                time.sleep(5)
                msgs = client.get_messages(bot, limit=1)
                for m in msgs:
                    if m.text and any(k in m.text.lower() for k in ["name", "father", "address", "phone"]):
                        log_data(f"Telegram-@{bot}", m.text, target)
    except Exception as e: print(f"{Fore.RED}[!] Telegram Error: {e}")

def main():
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID ULTIMATE OSINT FRAMEWORK (v3.0)         ")
    print(f"{Fore.RED}======================================================")
    
    tor = check_tor()
    proxy = "proxychains4 " if tor else ""
    target = input(f"\n{Fore.YELLOW}[+] Target (Phone/User/Email): ")
    
    # Layer 1: Surface & Gov Mirrors
    run_tool(f"googler --nocolor -n 5 -w gov.in \"{target}\"", "Gov-India", target)
    
    # Layer 2: Deep Web Tools
    run_tool(f"{proxy}maigret {target} --brief", "Maigret", target)
    run_tool(f"holehe {target} --only-used", "Holehe-Email", target)
    run_tool(f"social-analyzer --username {target} --mode fast", "Social-Analyzer", target)
    
    # Layer 3: Telegram Mirror (Screenshot Logic)
    telegram_scan(target)

    print(f"\n{Fore.GREEN}================ SCAN COMPLETE ================")
    print(f"{Fore.BLUE}Report Path: reports/{target}_master_report.txt")

if __name__ == "__main__":
    if not os.path.exists('reports'): os.makedirs('reports')
    main()
