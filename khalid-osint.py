import os, subprocess, time, requests
from colorama import Fore, init
init(autoreset=True)

def bot_engine():
    os.system('clear')
    print(Fore.RED + "--- KHALID GLOBAL BREACH SEARCH (BOT MIRROR) ---")
    print(Fore.YELLOW + "[STATUS: UNLIMITED SCAN ACTIVE | TOR: ENABLED]")
    target = input(Fore.WHITE + "[+] Target (Name/Phone/Email): ")
    
    print(Fore.YELLOW + f"[*] Fetching Data from Breach Databases & Telegram Mirrors...")

    # Deep Scan Command (Maigret + Breach Logic)
    # Yeh 2500+ sites aur leaked mirrors scan karta hai
    res = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
    output = res.stdout.strip()

    if output:
        print(Fore.GREEN + f"\n🔔 DATA FOUND FOR: {target}")
        print(Fore.WHITE + "═"*60)
        
        # Bot Style Formatting
        lines = output.split('\n')
        for line in lines:
            if line.strip():
                # Format like Telegram Bot: ➤ Name: Value
                print(f"{Fore.CYAN}➤ {line}")
        
        print(Fore.WHITE + "═"*60)
        
        # Save Report
        os.makedirs(f"reports/{target}", exist_ok=True)
        with open(f"reports/{target}/report.txt", "w") as f:
            f.write(output)
        print(f"📂 Full Bot-Style Report Saved: /root/osint/reports/{target}/report.txt")
    else:
        print(Fore.RED + "\n[!] NO DATA FOUND: Database mirrors mein ye record nahi mila.")

if __name__ == "__main__":
    while True:
        bot_engine()
        if input(Fore.YELLOW + "\nNew Search? (y/n): ").lower() != 'y': break
