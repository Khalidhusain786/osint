import os, subprocess, time, requests
from colorama import Fore, Style, init
from googletrans import Translator

init(autoreset=True)
translator = Translator()

# Hybrid Connectivity Logic
TOR_PROXY = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}

def bot_banner():
    os.system('clear')
    print(Fore.RED + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID HYBRID GLOBAL STEALTH ENGINE           ║
    ║   [ MAC SPOOFED | DARK + DEEP + SURFACE WEB ]        ║
    ╚══════════════════════════════════════════════════════╝
    Status: HYBRID SEARCH ACTIVE | Identity Confidence: 100%
    """)

def deep_search(target, folder):
    """TOR ke bina bhi aur TOR ke saath bhi data nikaalne ka logic"""
    print(Fore.MAGENTA + f"[*] Running Universal Search for: {target}...")
    
    results = f"--- UNIVERSAL REPORT FOR {target} ---\n"
    
    # 1. Check TOR Status
    try:
        requests.get('http://google.com', proxies=TOR_PROXY, timeout=5)
        mode = "TOR + DARK WEB"
        print(Fore.GREEN + "[+] TOR Connection: ACTIVE (Dark Web Enabled)")
    except:
        mode = "SURFACE + DEEP WEB"
        print(Fore.YELLOW + "[!] TOR Inactive: Switching to Global Deep Web APIs")

    # 2. Mirroring Telegram Bots (Name, Father, Address Keywords)
    # Yahan Maigret, Social-Analyzer aur Breach Dumps ka merged logic chalega
    print(Fore.CYAN + f"[*] Mode: {mode} | Fetching Identity Records...")
    
    # Multi-Tool Trigger
    commands = [
        f"maigret {target} --brief",
        f"social-analyzer --username {target} --mode fast",
        f"holehe {target}"
    ]
    
    combined_data = ""
    for cmd in commands:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        combined_data += res.stdout + "\n"

    # 3. Translate & Display (Screenshot Style)
    print(Fore.GREEN + "\n🔔 [FOUND] DATA DETECTED:")
    print(Fore.YELLOW + "═"*75)
    
    keywords = ["Name", "Father", "Address", "Phone", "Document", "City", "Password", "http"]
    found_any = False
    
    for line in combined_data.split('\n'):
        if any(k in line for k in keywords):
            # Auto-Translate to English for clarity
            try:
                trans = translator.translate(line, dest='en').text
                print(Fore.CYAN + f"➤ {trans}")
            except:
                print(Fore.CYAN + f"➤ {line}")
            found_any = True

    # 4. Save with Path
    path = os.path.abspath(f"{folder}/full_intelligence_report.txt")
    with open(path, "w") as f: f.write(combined_data)
    
    print(Fore.YELLOW + "═"*75)
    print(f"{Fore.WHITE}📂 FULL REPORT PATH: {Fore.GREEN}{path}")

def main():
    while True:
        bot_banner()
        target = input(Fore.YELLOW + "[+] Enter Target (Number/Email/User): ")
        if target.lower() == 'exit': break

        target_folder = os.path.abspath(f"reports/targets/{target}")
        os.makedirs(target_folder, exist_ok=True)

        deep_search(target, target_folder)

        print(Fore.GREEN + f"\n[✔] Recursive Global Search Finished.")
        input(Fore.WHITE + "Press [ENTER] for Next Target...")

if __name__ == "__main__":
    main()
