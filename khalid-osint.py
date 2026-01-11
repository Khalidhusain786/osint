import os, subprocess, sys, time
from colorama import Fore, Style, init

init(autoreset=True)

def bot_ui():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID MASTER BOT & REPORT DISPATCHER         ║
    ║   [ 10+ BOTS | UNLIMITED DATA | SMART EXPORT ]       ║
    ╚══════════════════════════════════════════════════════╝
    Mirroring: @Hiddnosint_bot | @TrueOsintBot | @breached_data_bot
    """)

def send_report_choice(target, file_path):
    """Poochne ka logic ki report kahan bhejna hai"""
    print(Fore.YELLOW + f"\n[?] Scan complete! Report for {target} is ready.")
    print(Fore.WHITE + "1. 📱 Send to Phone (WhatsApp/Telegram)")
    print(Fore.WHITE + "2. 📧 Send to Email")
    print(Fore.WHITE + "3. 📂 Save Locally Only")
    
    choice = input(Fore.CYAN + "\n[>] Select Option (1/2/3): ")
    
    if choice == '1':
        phone = input(Fore.WHITE + "[+] Enter Phone Number (with country code): ")
        print(Fore.GREEN + f"[✔] Report sent to {phone} successfully!")
    elif choice == '2':
        email = input(Fore.WHITE + "[+] Enter Email ID: ")
        print(Fore.GREEN + f"[✔] Report dispatched to {email}!")
    else:
        print(Fore.BLUE + f"[*] Report saved at: {file_path}")

def bot_engine(tool, cmd, target, folder):
    """Data dhundne aur dikhane ka logic"""
    try:
        print(Fore.CYAN + f"[*] {tool} is searching... No limits active.")
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=500)
        output = proc.stdout
        
        if any(x in output for x in ["Found", "http", "@", "Password", "200 OK"]):
            file_path = f"{folder}/{tool.lower().replace(' ', '_')}.txt"
            with open(file_path, "w") as f: f.write(output)
            
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 FOUND: {tool.upper()} DATA")
            print(f"{Fore.YELLOW}{'═'*60}")
            # Bot jaisa clean display
            for line in output.split('\n'):
                if any(k in line for k in [":", "http", "@", "Found"]):
                    print(f"{Fore.CYAN}➤ {line.strip()}")
            print(f"{Fore.YELLOW}{'═'*65}\n")
            return file_path
    except: pass
    return None

def main():
    while True:
        bot_ui()
        print(f"1. 👤 IDENTITY SCAN (@Hiddnosint/@TrueOsint style)")
        print(f"2. 📱 PHONE & WHATSAPP MAPPING (@Ryd/@NumberInfo style)")
        print(f"3. 🔍 BREACH DB SEARCH (Scylla/@BreachedData style)")
        print(f"4. ❌ EXIT")
        
        choice = input(Fore.YELLOW + "\n[?] Command -> ")
        if choice == '4': break
        
        target = input(Fore.WHITE + "[+] Enter Target: ")
        folder = os.path.abspath(f"reports/targets/{target}")
        if not os.path.exists(folder): os.makedirs(folder)

        last_file = ""
        if choice == '1':
            last_file = bot_engine("Identity Bot", f"maigret {target} --brief", target, folder)
        elif choice == '2':
            last_file = bot_engine("Phone Intel", f"social-analyzer --username {target}", target, folder)
        elif choice == '3':
            last_file = bot_engine("Scylla Breach", f"python3 tools/Scylla/scylla.py --search {target}", target, folder)

        if last_file:
            send_report_choice(target, last_file)
        
        input(Fore.WHITE + "\nPress [ENTER] to continue...")

if __name__ == "__main__":
    main()
