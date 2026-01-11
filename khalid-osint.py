import os, subprocess, time, yagmail
from colorama import Fore, Style, init

init(autoreset=True)

# Khalid's Config
MY_EMAIL = "kahyan292@gmail.com"
APP_KEY = "xxxx xxxx xxxx xxxx" # Apna 16-digit password yahan daal dein

def bot_banner():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║          KHALID MASTER OSINT - FINAL VER             ║
    ║      [ NO ERRORS | FAST SEARCH | DIRECT SEND ]       ║
    ╚══════════════════════════════════════════════════════╝
    """)

def direct_send(target, report_content, file_path):
    """Bina kisi prompt ke email bhejne ka option"""
    choice = input(Fore.YELLOW + "\n[?] Data mil gaya! Kya email bhej doon? (y/n): ").lower()
    if choice == 'y':
        print(Fore.MAGENTA + "[*] Sending to kahyan292@gmail.com...")
        try:
            yag = yagmail.SMTP(MY_EMAIL, APP_KEY)
            yag.send(to=MY_EMAIL, subject=f"OSINT: {target}", contents=report_content, attachments=file_path)
            print(Fore.GREEN + "[✔] Sent Successfully!")
        except:
            print(Fore.RED + "[!] Email Error: Check App Password.")

def main():
    while True:
        bot_banner()
        target = input(Fore.WHITE + "[+] Enter Target (Number/User): ")
        if target.lower() == 'exit': break

        print(Fore.CYAN + f"[*] Searching databases for {target}...")
        
        # Using Maigret for deep search
        res = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
        output = res.stdout

        # Filter and Show (Like Telegram Bot Screenshot)
        print(Fore.GREEN + "\n🔔 FOUND DATA:")
        print(Fore.YELLOW + "═"*60)
        
        # Displaying key identity info
        if output:
            print(Fore.CYAN + output)
        else:
            print(Fore.RED + "[-] No direct match found in this layer.")
        
        print(Fore.YELLOW + "═"*60)
        
        # Save and Dispatch
        folder = f"reports/{target}"
        os.makedirs(folder, exist_ok=True)
        path = os.path.abspath(f"{folder}/report.txt")
        with open(path, "w") as f: f.write(output)
        
        print(f"📂 Saved at: {path}")
        direct_send(target, output, path)
        
        input(Fore.WHITE + "\nPress [ENTER] to continue...")

if __name__ == "__main__":
    main()
