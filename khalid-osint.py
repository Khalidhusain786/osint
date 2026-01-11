import os, subprocess, time, sys
from colorama import Fore, Style, init

init(autoreset=True)

def bot_banner():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID 6-LAYER GLOBAL SEARCH ENGINE           ║
    ║   [ TARGET | INFRA | LEAKS | TELEGRAM MIRROR ]       ║
    ╚══════════════════════════════════════════════════════╝
    Status: INFINITE SEARCH MODE | Path-Show: ENABLED
    """)

def process_and_show_path(layer_name, output, target, folder):
    """Data dhundne, screen par dikhane aur path batane ka logic"""
    # Key details jo Telegram bots dikhaate hain
    keywords = ["Name", "Father", "Address", "Phone", "Document", "City", "Password", "http", "User"]
    
    if any(k in output for k in keywords):
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 [FOUND] {layer_name.upper()} DATA DETECTED")
        print(f"{Fore.YELLOW}{'═'*75}")
        
        # Displaying like Telegram Bot
        for line in output.split('\n'):
            if any(k in line for k in keywords):
                print(Fore.CYAN + f"➤ {line.strip()}")
        
        # Saving and Showing Absolute Path
        file_path = os.path.abspath(f"{folder}/{layer_name.lower()}.txt")
        with open(file_path, "w") as f:
            f.write(output)
        
        print(f"{Fore.YELLOW}{'═'*75}")
        print(f"{Fore.WHITE}📂 LOCATION: {Fore.GREEN}{file_path}\n")
        return True
    return False

def main():
    while True: # Infinite Target Loop
        bot_banner()
        target = input(Fore.YELLOW + "[+] Enter Target (Number/Email/User): ")
        if target.lower() == 'exit': break

        # Create target-specific folder
        target_folder = os.path.abspath(f"reports/targets/{target}")
        os.makedirs(target_folder, exist_ok=True)
        
        print(Fore.MAGENTA + f"\n[*] Starting Recursive Global Search for: {target}...")
        
        # Layer 1: Identity & Social (@Hiddnosint / @TrueOsint Style)
        res1 = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
        process_and_show_path("Identity_Layer", res1.stdout, target, target_folder)

        # Layer 2: Phone & Mapping (India Special @number_infobot)
        res2 = subprocess.run(f"social-analyzer --username {target} --mode fast", shell=True, capture_output=True, text=True)
        process_and_show_path("Phone_Social_Footprint", res2.stdout, target, target_folder)

        # Layer 3: Leaks & Dark Intel (@breached_data_bot)
        res3 = subprocess.run(f"holehe {target}", shell=True, capture_output=True, text=True)
        process_and_show_path("Leak_Intelligence", res3.stdout, target, target_folder)

        # Layer 4: Infrastructure (WHOIS/DNS)
        res4 = subprocess.run(f"whois {target}", shell=True, capture_output=True, text=True)
        process_and_show_path("Infra_OSINT", res4.stdout, target, target_folder)

        print(Fore.GREEN + f"\n[✔] Recursive Search Finished for {target}.")
        input(Fore.WHITE + "Press [ENTER] for another target...")

if __name__ == "__main__":
    main()
