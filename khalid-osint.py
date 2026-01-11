import os, subprocess, sys, time, json
from colorama import Fore, Style, init

init(autoreset=True)

def bot_banner():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID OSINT BOT - NO LIMIT EDITION           ║
    ║   [ SCYLLA | HIDDN | BREACHED | SOCIAL | PHONE ]     ║
    ╚══════════════════════════════════════════════════════╝
    Mirroring: @Hiddnosint_bot | @breached_data_bot
    """)

def display_bot_data(tool, output, folder):
    """Telegram Bot ki tarah data ko screen par show karne ka logic"""
    if any(x in output for x in ["Found", "http", "@", "Password", "200 OK", "User"]):
        file_path = f"{folder}/{tool.lower().replace(' ', '_')}.txt"
        with open(file_path, "w") as f:
            f.write(output)

        print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 [FOUND] DATA FROM {tool.upper()}")
        print(f"{Fore.WHITE}📂 Path: {file_path}")
        print(f"{Fore.YELLOW}{'═'*60}")
        
        # Telegram Bot jaisa representation
        lines = output.split('\n')
        for line in lines:
            if ":" in line or "http" in line:
                # Clean up and show like a bot message
                print(f"{Fore.CYAN}➤ {line.strip()}")
        
        print(f"{Fore.YELLOW}{'═'*60}\n")
        return True
    return False

def run_scylla(target, folder):
    """Scylla Database Search Logic"""
    print(Fore.MAGENTA + "[*] Searching Scylla Breach Database...")
    cmd = f"python3 tools/Scylla/scylla.py --search {target}"
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=500)
        display_bot_data("Scylla DB", proc.stdout, folder)
    except:
        print(Fore.RED + "[!] Scylla Error. Check installation.")

def main():
    while True: # Unlimited Loop - Kabhi band nahi hoga
        bot_banner()
        print(f"1. 👤 IDENTITY BREACH (Telegram Bot Style)")
        print(f"2. 📱 PHONE & WHATSAPP MAPPING")
        print(f"3. 📁 BROWSE PREVIOUS REPORTS")
        print(f"4. ❌ EXIT")
        
        choice = input(Fore.YELLOW + "\n[?] Select Option -> ")
        if choice == '4': break
        
        target = input(Fore.WHITE + "[+] Enter Target (Email/User/Number): ")
        target_folder = os.path.abspath(f"reports/targets/{target}")
        if not os.path.exists(target_folder): os.makedirs(target_folder)

        if choice == '1':
            # Scylla Database (Leaks)
            run_scylla(target, target_folder)
            
            # Social Search (Telegram style)
            print(Fore.MAGENTA + "[*] Crawling Social Media Profiles...")
            cmd_maigret = f"maigret {target} --brief"
            proc_m = subprocess.run(cmd_maigret, shell=True, capture_output=True, text=True)
            display_bot_data("Social Links", proc_m.stdout, target_folder)

            # Email Breach
            cmd_holehe = f"holehe {target}"
            proc_h = subprocess.run(cmd_holehe, shell=True, capture_output=True, text=True)
            display_bot_data("Email Breach", proc_h.stdout, target_folder)

        elif choice == '2':
            # Phone Intel logic
            print(Fore.MAGENTA + "[*] Fetching Carrier & Social Intel...")
            cmd_p = f"social-analyzer --username {target}" # Phone logic here
            proc_p = subprocess.run(cmd_p, shell=True, capture_output=True, text=True)
            display_bot_data("Phone Intelligence", proc_p.stdout, target_folder)

        print(Fore.GREEN + f"\n[✔] Scan Finished for: {target}")
        input(Fore.WHITE + "Press [ENTER] to search another target...")

if __name__ == "__main__":
    main()
