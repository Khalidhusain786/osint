import os, subprocess, time, yagmail
from colorama import Fore, Style, init
from fpdf import FPDF

init(autoreset=True)

# Aapki Details
MY_EMAIL = "kahyan292@gmail.com"
APP_PASSWORD = "xxxx xxxx xxxx xxxx" # Apna 16-digit App Password yahan daalein

def bot_banner():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID ALL-IN-ONE BOT MIRROR ENGINE           ║
    ║   [ BREACH | IDENTITY | SOCIAL | NO LIMITS ]         ║
    ╚══════════════════════════════════════════════════════╝
    Mirroring: @osint_bot_link | @Hiddnosint_bot | @TrueOsintBot
    """)

def telegram_style_found(tool, output):
    """Data ko screenshot wale format mein dikhane ka logic"""
    # Checking for real identity data keywords
    keywords = ["Name", "Father", "Address", "Phone", "Document", "http", "Password"]
    if any(k in output for k in keywords):
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 FOUND DATA DETECTED FROM {tool.upper()}")
        print(f"{Fore.YELLOW}{'═'*65}")
        
        # Filtering and showing like the screenshot
        for line in output.split('\n'):
            line = line.strip()
            if any(k in line for k in keywords):
                print(f"{Fore.CYAN}➤ {line}")
        
        print(f"{Fore.YELLOW}{'═'*65}")
        return True
    return False

def main():
    while True: # Infinite Loop - Jab tak aap band na karein
        bot_banner()
        print("1. 👤 IDENTITY DEEP SEARCH (Screenshot Mode)\n2. 📱 PHONE & WHATSAPP MAPPING\n3. ❌ EXIT")
        choice = input(Fore.YELLOW + "\n[?] Select Action -> ")
        if choice == '3': break
        
        target = input(Fore.WHITE + "[+] Enter Target (Number/Email/User): ")
        print(Fore.MAGENTA + f"\n[*] Engaging all merged bots for: {target}")

        # 1. Breach DB (Scylla Logic)
        scylla_cmd = f"python3 tools/Scylla/scylla.py --search {target}"
        res_s = subprocess.run(scylla_cmd, shell=True, capture_output=True, text=True)
        found_1 = telegram_style_found("Breach Scan", res_s.stdout)

        # 2. Social Mapping (Maigret Logic)
        maigret_cmd = f"maigret {target} --brief"
        res_m = subprocess.run(maigret_cmd, shell=True, capture_output=True, text=True)
        found_2 = telegram_style_found("Hiddn Search", res_m.stdout)

        if found_1 or found_2:
            ask = input(Fore.WHITE + "\n[?] Send this found data to kahyan292@gmail.com? (y/n): ")
            if ask.lower() == 'y':
                print(Fore.GREEN + "[*] Dispatching PDF Report...")
                # PDF/Email logic yahan trigger hoga
        
        input(Fore.WHITE + "\nScan finished. Press [ENTER] for next target...")

if __name__ == "__main__":
    main()
