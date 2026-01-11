import os, subprocess, sys, time
from colorama import Fore, Style, init

init(autoreset=True)

def bot_interface():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID UNLIMITED OSINT BOT ENGINE             ║
    ║   [ NO LIMIT | NO ERRORS | TELEGRAM BOT STYLE ]      ║
    ╚══════════════════════════════════════════════════════╝
    Mirroring: @Hiddnosint_bot | @breached_data_bot | @osint_bot_link
    """)

def telegram_style_display(tool_name, output, target, folder):
    """Found data ko table format mein screen par dikhayega"""
    if any(x in output for x in ["Found", "http", "Password", "User", "Active", "@"]):
        file_path = f"{folder}/{tool_name.lower().replace(' ', '_')}.txt"
        with open(file_path, "w") as f:
            f.write(output)

        print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 FOUND: {tool_name.upper()} DATA DETECTED!")
        print(f"{Fore.WHITE}📂 Path: {file_path}")
        print(f"{Fore.YELLOW}{'═'*65}")
        
        # Display clean data like a Bot response
        for line in output.split('\n'):
            if any(k in line for k in [":", "http", "@", "Found"]):
                print(f"{Fore.CYAN}➤ {line.strip()}")
        print(f"{Fore.YELLOW}{'═'*65}\n")

def main():
    while True: # Infinite Loop - Jab tak aap na rokein
        bot_interface()
        print(f"1. 👤 DEEP IDENTITY SCAN (Telegram Bot Logic)\n2. 📱 PHONE & WHATSAPP MAPPING\n3. 📁 VIEW ALL SAVED DATA\n4. ❌ EXIT")
        
        choice = input(Fore.YELLOW + "\n[?] Select Action -> ")
        if choice == '4': break
        
        target = input(Fore.WHITE + "[+] Enter Target (Email/User/Number): ")
        folder = os.path.abspath(f"reports/targets/{target}")
        if not os.path.exists(folder): os.makedirs(folder)

        if choice == '1':
            print(Fore.MAGENTA + "[*] Crawling Databases (Scylla/Social/Breach)...")
            # Scylla Force Run
            scylla_cmd = f"python3 tools/Scylla/scylla.py --search {target}"
            proc_s = subprocess.run(scylla_cmd, shell=True, capture_output=True, text=True)
            telegram_style_display("Scylla Breach", proc_s.stdout, target, folder)
            
            # Social Media Hiddn Logic
            proc_m = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
            telegram_style_display("Social Presence", proc_m.stdout, target, folder)

        elif choice == '2':
            print(Fore.MAGENTA + "[*] Mapping Phone & Linked Socials...")
            proc_p = subprocess.run(f"social-analyzer --username {target}", shell=True, capture_output=True, text=True)
            telegram_style_display("Phone Intel", proc_p.stdout, target, folder)

        print(Fore.GREEN + f"[✔] All tools finished for {target}.")
        input(Fore.WHITE + "Press [ENTER] to continue with another search...")

if __name__ == "__main__":
    main()
