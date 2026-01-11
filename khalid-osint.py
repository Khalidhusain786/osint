import os, subprocess, sys, time
from colorama import Fore, Style, init

init(autoreset=True)

def bot_banner():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID OSINT BOT ENGINE (UNLIMITED)           ║
    ║   [ DEEP BREACH | IDENTITY MAPPING | NO LIMITS ]     ║
    ╚══════════════════════════════════════════════════════╝
    Mirroring: @Hiddnosint_bot | @breached_data_bot
    """)

def bot_found_display(tool, data, target, folder):
    """Telegram Bot style data display logic"""
    file_path = f"{folder}/{tool.lower().replace(' ', '_')}.txt"
    with open(file_path, "w") as f:
        f.write(data)

    print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 FOUND DATA DETECTED [{tool}]")
    print(f"{Fore.WHITE}📂 File: {file_path}")
    print(f"{Fore.YELLOW}{'═'*50}")
    
    # Telegram Bot ki tarah important details highlight karna
    lines = data.split('\n')[:15] # Sirf pehli 15 lines ka preview
    for line in lines:
        if any(k in line for k in ["http", "Email", "Password", "User", "Found"]):
            print(f"{Fore.CYAN}➤ {line.strip()}")
    print(f"{Fore.YELLOW}{'═'*50}\n")

def run_bot_logic(name, cmd, target, folder):
    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=500)
        output = proc.stdout
        # Bot style filtering
        if any(x in output for x in ["Found", "http", "registered", "Active", "200 OK", "@"]):
            bot_found_display(name, output, target, folder)
    except:
        pass

def main():
    while True:
        bot_banner()
        print(f"1. 👤 IDENTITY BREACH (Telegram Bot Style - Deep Scan)")
        print(f"2. 📱 PHONE ENRICHMENT (India & Global Database)")
        print(f"3. 📁 OPEN ALL SAVED EVIDENCE")
        print(f"4. ❌ EXIT")
        
        choice = input(Fore.YELLOW + "\n[?] Select Command -> ")
        if choice == '4': break
        
        target = input(Fore.WHITE + "[+] Enter Target (Email/Username/Phone): ")
        target_folder = os.path.abspath(f"reports/targets/{target}")
        if not os.path.exists(target_folder): os.makedirs(target_folder)

        if choice == '1':
            print(Fore.MAGENTA + f"\n[*] Engaging Deep Crawlers for {target}...")
            # Integrating Scylla, Sherlock, Maigret, and SocialMediaToolkit
            run_bot_logic("Breach DB (Scylla)", f"scylla --search {target}", target, target_folder)
            run_bot_logic("Social Presence", f"maigret {target} --brief", target, target_folder)
            run_bot_logic("Account Discovery", f"python3 tools/sherlock/sherlock/sherlock.py {target} --timeout 1", target, target_folder)
            run_bot_logic("Email Recon (Holehe)", f"holehe {target}", target, target_folder)
            
        elif choice == '2':
            print(Fore.MAGENTA + f"\n[*] Analyzing Phone Metadata & Social Links...")
            run_bot_logic("Phone-Tell", f"phonetell {target}", target, target_folder)
            run_bot_logic("Phomber", f"phomber --number {target}", target, target_folder)

        print(Fore.GREEN + f"[*] Scan Finished. All findings stored in: {target_folder}")
        time.sleep(5)

if __name__ == "__main__":
    main()
