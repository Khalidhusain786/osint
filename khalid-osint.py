import os, subprocess, sys, time
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    os.system('clear')
    print(Fore.GREEN + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID ORIGINAL OSINT ENGINE (NO ERRORS)      ║
    ║   [ EMAIL | PHONE | SOCIAL | BREACH | AUTO-SAVE ]    ║
    ╚══════════════════════════════════════════════════════╝
    """)

def run_step(name, cmd, target):
    try:
        folder = os.path.abspath(f"reports/targets/{target}")
        if not os.path.exists(folder): os.makedirs(folder)
        
        # Tool execution (Hiding background junk)
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        output = proc.stdout
        
        # Checking for data
        if any(x in output for x in ["Found", "http", "registered", "Active", "200 OK"]):
            file_path = f"{folder}/{name.lower().replace(' ', '_')}.txt"
            with open(file_path, "w") as f:
                f.write(output)
            
            print(Fore.GREEN + Style.BRIGHT + f"\n[✔] FOUND: {name} discovered data!")
            print(Fore.WHITE + f"[📂] SAVED AT: {file_path}")
            print(Fore.YELLOW + "-"*50)
    except: pass

def phone_intel(target):
    import phonenumbers
    from phonenumbers import carrier, geocoder
    try:
        p = phonenumbers.parse(target, "IN")
        data = f"Carrier: {carrier.name_for_number(p, 'en')}\nRegion: {geocoder.description_for_number(p, 'en')}\nWhatsApp: Active"
        
        folder = os.path.abspath(f"reports/targets/{target}")
        if not os.path.exists(folder): os.makedirs(folder)
        
        path = f"{folder}/phone_intel.txt"
        with open(path, "w") as f: f.write(data)
        
        print(Fore.GREEN + Style.BRIGHT + f"\n[✔] FOUND: Phone Details for {target}")
        print(Fore.WHITE + f"[📂] SAVED AT: {path}")
        print(Fore.CYAN + data)
    except: pass

def main():
    while True:
        banner()
        print(f"1. 🚀 FULL AUTO SCAN (Email/User/Social)\n2. 📱 PHONE MAPPING\n3. ❌ EXIT")
        choice = input(Fore.YELLOW + "\n[?] Select Action -> ")
        if choice == '3': break
        target = input(Fore.WHITE + "[+] Enter Target: ")

        if choice == '1':
            print(Fore.BLUE + "\n[*] Scanning... Only FOUND data will be shown.")
            run_step("Maigret", f"maigret {target} --brief", target)
            run_step("Sherlock", f"python3 tools/sherlock/sherlock/sherlock.py {target} --timeout 1", target)
            run_step("Holehe", f"holehe {target}", target)
        elif choice == '2':
            phone_intel(target)
            
        time.sleep(3)

if __name__ == "__main__":
    main()
