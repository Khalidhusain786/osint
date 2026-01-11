import os, subprocess, time, yagmail
from colorama import Fore, Style, init
from fpdf import FPDF

init(autoreset=True)

# Email Setup
MY_EMAIL = "kahyan292@gmail.com"
APP_PASSWORD = "xxxx xxxx xxxx xxxx" # Apna App Password yahan daalein

def bot_banner():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID ULTIMATE ALL-IN-ONE OSINT BOT          ║
    ║   [ MIRRORING ALL TELEGRAM BOTS | FULL DATA ]        ║
    ╚══════════════════════════════════════════════════════╝
    Status: All Tools Connected | No Limits Active
    """)

def show_and_save_data(tool_name, output, target, folder_path):
    """Data dikhane aur uska path show karne ka logic"""
    keywords = ["Name", "Father", "Address", "Phone", "Document", "City", "Password", "http"]
    
    if any(k in output for k in keywords):
        # 1. Screen par Data dikhana (Telegram Style)
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 [FOUND] DATA FROM: {tool_name.upper()}")
        print(f"{Fore.YELLOW}{'═'*65}")
        for line in output.split('\n'):
            if any(k in line for k in keywords):
                print(f"{Fore.CYAN}➤ {line.strip()}")
        print(f"{Fore.YELLOW}{'═'*65}")

        # 2. File Save karna aur Path dikhana
        file_name = f"{tool_name.lower().replace(' ', '_')}.txt"
        full_path = os.path.join(folder_path, file_name)
        with open(full_path, "w") as f:
            f.write(output)
        
        print(f"{Fore.WHITE}📂 File Saved At: {Fore.GREEN}{full_path}")
        return full_path
    return None

def main():
    while True:
        bot_banner()
        target = input(Fore.YELLOW + "[+] Enter Target (Number/Email/User): ")
        if target.lower() == 'exit': break

        # Create unique folder for target
        target_folder = os.path.abspath(f"reports/targets/{target}")
        os.makedirs(target_folder, exist_ok=True)
        
        print(Fore.MAGENTA + f"\n[*] Starting Deep Scan for {target} using all integrated bots...")

        # --- 1. BREACH SCAN (@osint_bot_link & @breached_data_bot style) ---
        scylla_cmd = f"python3 tools/Scylla/scylla.py --search {target}"
        res_s = subprocess.run(scylla_cmd, shell=True, capture_output=True, text=True)
        path1 = show_and_save_data("Breach Bot", res_s.stdout, target, target_folder)

        # --- 2. IDENTITY MAPPING (@Hiddnosint_bot & @TrueOsintBot style) ---
        maigret_cmd = f"maigret {target} --brief"
        res_m = subprocess.run(maigret_cmd, shell=True, capture_output=True, text=True)
        path2 = show_and_save_data("Identity Bot", res_m.stdout, target, target_folder)

        # --- 3. PHONE INTEL (@number_infobot & @Ryd_osintbot style) ---
        # Social-analyzer mapping for phone records
        phone_cmd = f"social-analyzer --username {target} --mode fast"
        res_p = subprocess.run(phone_cmd, shell=True, capture_output=True, text=True)
        path3 = show_and_save_data("Phone Intel Bot", res_p.stdout, target, target_folder)

        if path1 or path2 or path3:
            choice = input(Fore.WHITE + "\n[?] Send found reports to kahyan292@gmail.com? (y/n): ")
            if choice.lower() == 'y':
                print(Fore.GREEN + "[*] Dispatching all data to your email...")

        input(Fore.WHITE + "\nScan Finished. Press [ENTER] to continue...")

if __name__ == "__main__":
    main()
