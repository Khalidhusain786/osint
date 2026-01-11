import os, subprocess, sys, time
from colorama import Fore, Style, init

init(autoreset=True)

def bot_ui():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID UNLIMITED BOT INTELLIGENCE ENGINE      ║
    ║   [ NO LIMITS | NO ERRORS | ALL BOTS INTEGRATED ]    ║
    ╚══════════════════════════════════════════════════════╝
    Status: Mirroring @Hiddnosint_bot | @TrueOsintBot | @Ryd_osintbot
    """)

def bot_found_display(tool, output, target, folder):
    """Telegram Bot ki tarah data ko screen par dikhayega"""
    # Sirf Found hone par alert dega
    if any(x in output for x in ["Found", "http", "Password", "Active", "Success", "@", "200 OK"]):
        file_path = f"{folder}/{tool.lower().replace(' ', '_')}.txt"
        with open(file_path, "w") as f:
            f.write(output)

        print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 [FOUND] DATA DETECTED FROM {tool.upper()}")
        print(f"{Fore.WHITE}📂 Path: {file_path}")
        print(f"{Fore.YELLOW}{'═'*65}")
        
        # Display clean data like a Bot response
        for line in output.split('\n'):
            if any(k in line for k in [":", "http", "@", "Found", "User"]):
                print(f"{Fore.CYAN}➤ {line.strip()}")
        print(f"{Fore.YELLOW}{'═'*65}\n")
        return True
    return False

def main():
    while True: # Infinite Loop - Jab tak aap na rokein
        bot_ui()
        print(f"1. 👤 IDENTITY & SOCIAL SCAN (Bot Style Logic)")
        print(f"2. 📱 PHONE & WHATSAPP INTEL (Ryd/TrueOsint Style)")
        print(f"3. 🔍 DEEP BREACH SEARCH (Scylla/BreachedData Style)")
        print(f"4. ❌ EXIT ENGINE")
        
        choice = input(Fore.YELLOW + "\n[?] Select Command -> ")
        if choice == '4': break
        
        target = input(Fore.WHITE + "[+] Enter Target (Number/Email/User): ")
        folder = os.path.abspath(f"reports/targets/{target}")
        if not os.path.exists(folder): os.makedirs(folder)

        if choice == '1':
            print(Fore.MAGENTA + "[*] Crawling Social & Identity Databases...")
            # Maigret Integration
            proc_m = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
            bot_found_display("Social Intelligence", proc_m.stdout, target, folder)
            
        elif choice == '2':
            print(Fore.MAGENTA + "[*] Mapping Phone Registries & WhatsApp Status...")
            # Social Analyzer for Numbers
            proc_p = subprocess.run(f"social-analyzer --username {target}", shell=True, capture_output=True, text=True)
            bot_found_display("Phone/Social Intel", proc_p.stdout, target, folder)

        elif choice == '3':
            print(Fore.MAGENTA + "[*] Searching Global Breach Databases (No Limits)...")
            # Scylla Force Run
            scylla_cmd = f"python3 tools/Scylla/scylla.py --search {target}"
            proc_s = subprocess.run(scylla_cmd, shell=True, capture_output=True, text=True)
            bot_found_display("Scylla Breach DB", proc_s.stdout, target, folder)

        print(Fore.GREEN + f"\n[✔] Scan Finished. Results stored in: {folder}")
        input(Fore.WHITE + "Press [ENTER] to continue with next target...")

if __name__ == "__main__":
    main()
