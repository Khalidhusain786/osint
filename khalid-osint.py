import os, subprocess, sys, time
from colorama import Fore, Style, init

init(autoreset=True)

def bot_banner():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID OSINT MASTER (NO-LIMIT EDITION)        ║
    ║   [ UNLIMITED SEARCH | NO TIMEOUT | AUTO-REPAIR ]    ║
    ╚══════════════════════════════════════════════════════╝
    Status: Mirroring @Hiddnosint_bot | @osint_bot_link
    """)

def bot_engine(name, cmd, target):
    """Found data ko screen par highlight karega aur path batayega"""
    try:
        folder = os.path.abspath(f"reports/targets/{target}")
        if not os.path.exists(folder): os.makedirs(folder)
        
        print(Fore.CYAN + f"[*] {name} is crawling for {target}...")
        
        # Deep Scan (No Limit)
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)
        output = proc.stdout
        
        # Sirf Found data ka bot-style display
        if any(x in output for x in ["Found", "registered", "http", "@", "Password", "200 OK"]):
            file_path = f"{folder}/{name.lower().replace(' ', '_')}.txt"
            with open(file_path, "w") as f:
                f.write(output)
            
            print(Fore.GREEN + Style.BRIGHT + f"\n🔔 ALERT: DATA FOUND BY {name}!")
            print(Fore.WHITE + f"📂 LOCATION: {file_path}")
            print(Fore.YELLOW + "═" * 50)
            
            # Data Preview (Jaise Bot dikhata hai)
            preview = "\n".join([line for line in output.split('\n') if any(k in line for k in ["http", "@", "Found", "User"])][:10])
            print(Fore.CYAN + preview)
            print(Fore.YELLOW + "═" * 50 + "\n")
    except:
        pass

def main():
    while True: # Yeh loop tool ko band nahi hone dega
        bot_banner()
        print(f"1. 👤 UNLIMITED IDENTITY SCAN (All Bots Logic)")
        print(f"2. 📱 UNLIMITED PHONE INTEL (Phomber/Phunter)")
        print(f"3. 📁 BROWSE ALL FOUND DATA")
        print(f"4. ❌ EXIT TOOL")
        
        choice = input(Fore.YELLOW + "\n[?] Select Command -> ")
        
        if choice == '4':
            print(Fore.RED + "[!] Exiting Khalid OSINT Suite...")
            break
            
        target = input(Fore.WHITE + "[+] Enter Target (Email/Number/User): ")

        if choice == '1':
            print(Fore.MAGENTA + "\n[!] Engaging Multi-Bot Crawlers...")
            bot_engine("Scylla Breach", f"scylla --search {target}", target)
            bot_engine("Social Analyzer", f"social-analyzer --username {target}", target)
            bot_engine("Maigret", f"maigret {target} --brief", target)
            bot_engine("Email Recon", f"holehe {target}", target)
            
        elif choice == '2':
            print(Fore.MAGENTA + "\n[!] Engaging Phone Intel Engines...")
            bot_engine("Phunter", f"phunter {target}", target)
            bot_engine("Phomber", f"phomber --number {target}", target)
            
        elif choice == '3':
            os.system(f"ls -R reports/targets/")
        
        print(Fore.GREEN + f"\n[✔] All Scans Finished for {target}.")
        input(Fore.WHITE + "Press Enter to continue with next target...")

if __name__ == "__main__":
    main()
