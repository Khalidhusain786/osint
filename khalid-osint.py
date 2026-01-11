import os, subprocess, time, yagmail
from colorama import Fore, Style, init
from fpdf import FPDF

init(autoreset=True)

# Email Setup for Khalid
MY_EMAIL = "kahyan292@gmail.com"
APP_PASSWORD = "xxxx xxxx xxxx xxxx" # Apna 16-digit App Password yahan daalein

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'CONFIDENTIAL OSINT IDENTITY REPORT', 0, 1, 'C')

def extract_and_display(tool_name, output, target):
    """Telegram Bot style format (Name, Address, Phone)"""
    if any(k in output for k in ["Found", "http", "@", "200 OK", "Address"]):
        print(f"\n{Fore.GREEN}{Style.BRIGHT}🔔 [FOUND] DEEP DATA DETECTED: {tool_name}")
        print(f"{Fore.YELLOW}{'═'*65}")
        
        # Format output to look like the Telegram Bot screenshot
        lines = output.split('\n')
        for line in lines:
            if any(key in line for key in ["Name", "Father", "Address", "Phone", "Document", "http"]):
                print(f"{Fore.CYAN}➤ {line.strip()}")
        
        print(f"{Fore.YELLOW}{'═'*65}")
        return True
    return False

def main():
    while True:
        os.system('clear')
        print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID IDENTITY BOT (DEEP SCAN MODE)          ║
    ║   [ MIRRORING: @osint_bot_link | @Hiddnosint ]       ║
    ╚══════════════════════════════════════════════════════╝
        """)
        print("1. 👤 FULL IDENTITY SEARCH (Name/Address/Leaks)\n2. 📱 PHONE MAPPING\n3. ❌ EXIT")
        choice = input(Fore.YELLOW + "\n[?] Select Action -> ")
        if choice == '3': break
        
        target = input(Fore.WHITE + "[+] Enter Target (Number/Email/User): ")
        folder = f"reports/targets/{target}"
        os.makedirs(folder, exist_ok=True)

        print(Fore.MAGENTA + f"\n[*] Querying Deep Databases for {target}...")
        
        # Scylla Deep Search (Screenshot fix)
        scylla_cmd = f"python3 tools/Scylla/scylla.py --search {target}"
        res = subprocess.run(scylla_cmd, shell=True, capture_output=True, text=True)
        found = extract_and_display("Breach DB", res.stdout, target)
        
        # Social Detail mapping
        maigret_cmd = f"maigret {target} --brief"
        res_m = subprocess.run(maigret_cmd, shell=True, capture_output=True, text=True)
        extract_and_display("Identity Mapping", res_m.stdout, target)

        if found:
            # Ask for Email Dispatch
            ask = input(Fore.WHITE + "\n[?] Send PDF Report to kahyan292@gmail.com? (y/n): ")
            if ask.lower() == 'y':
                print(Fore.GREEN + "[✔] Generating PDF and Sending to Khalid...")
                # PDF & Email logic here...
        
        input(Fore.WHITE + "\nScan complete. Press Enter for next target...")

if __name__ == "__main__":
    main()
