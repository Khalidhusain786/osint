import os, subprocess, time
from colorama import Fore, init
init(autoreset=True)

def bot_engine():
    os.system('clear')
    print(Fore.RED + "--- KHALID GLOBAL HIDDEN SEARCH (TELEGRAM STYLE) ---")
    target = input(Fore.WHITE + "[+] Enter Target (Name/User/Email): ")
    print(Fore.YELLOW + f"[*] Scanning Deep & Dark Web Layers for {target}...")

    # Powerful Search Command (Deep Scan)
    # Isme hum Maigret use kar rahe hain jo Telegram bot ki tarah results deta hai
    res = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
    
    output = res.stdout.strip()

    # Logic: Data hone par hi show karega
    if output:
        print(Fore.GREEN + f"\n🔔 DATA FOUND FOR: {target}")
        print(Fore.WHITE + "═"*60)
        for line in output.split('\n'):
            if line.strip():
                print(f"{Fore.CYAN}➤ {line}")
        print(Fore.WHITE + "═"*60)
        
        # Save results
        os.makedirs(f"reports/{target}", exist_ok=True)
        with open(f"reports/{target}/report.txt", "w") as f:
            f.write(output)
        print(f"📂 Report Saved: /root/osint/reports/{target}/report.txt")
    else:
        print(Fore.RED + "\n[!] NO DATA FOUND: Internet aur Hidden layers par koi record nahi mila.")

if __name__ == "__main__":
    while True:
        bot_engine()
        retry = input(Fore.YELLOW + "\nNew Search? (y/n): ")
        if retry.lower() != 'y': break
