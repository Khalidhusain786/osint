import os
import subprocess
import phonenumbers
from phonenumbers import carrier, geocoder
from colorama import Fore, Style

# Developer: Khalid Husain (@khalidhusain786)

def banner():
    os.system('clear')
    if not os.path.exists("reports"): os.makedirs("reports")
    print(Fore.GREEN + f"""
    #########################################################
    #              KHALID PERFECT OSINT FRAMEWORK           #
    #      Developed by: Khalid Husain (@khalidhusain786)   #
    #########################################################
    """ + Style.RESET_ALL)

def run_osint(cmd, target):
    report_file = f"reports/{target.replace('@','_')}_scan.txt"
    print(Fore.YELLOW + f"[*] Engine Working on: {target}..." + Style.RESET_ALL)
    try:
        with open(report_file, "a") as f:
            f.write(f"\n--- Scan: {cmd} ---\n")
            # Direct execution fix
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(result.stdout)
            f.write(result.stdout)
    except Exception as e:
        print(Fore.RED + f"[!] Error executing {cmd}: {e}")

def main():
    while True:
        banner()
        print("1. 📧 Email & Social Presence (Insta/FB/Gmail)")
        print("2. 👤 Username Search (3000+ Social Sites)")
        print("3. 📱 Phone Intel (Carrier/Region/WhatsApp)")
        print("4. 🌐 Web Recon (Domain/Subdomains)")
        print("5. ❌ Exit")
        
        choice = input(Fore.CYAN + "\n[?] Select Option: " + Style.RESET_ALL)
        if choice == '5': break
        target = input(Fore.WHITE + "[+] Target (Value): " + Style.RESET_ALL)

        if choice == '1':
            # Fixed commands for Kali 2024/25
            run_osint(f"python3 -m holehe.cli {target}", target)
            run_osint(f"haveibeenpwned {target}", target)
        elif choice == '2':
            run_osint(f"maigret {target} --brief", target)
            run_osint(f"python3 $HOME/sherlock/sherlock.py {target}", target)
        elif choice == '3':
            try:
                p = phonenumbers.parse(target, "IN")
                print(Fore.GREEN + f"[+] Carrier: {carrier.name_for_number(p, 'en')}")
                print(f"[+] Region: {geocoder.description_for_number(p, 'en')}")
            except: print(Fore.RED + "[!] Use format: +91xxxxxxxxxx")
        elif choice == '4':
            run_osint(f"photon -u https://{target}", target)

        input(Fore.GREEN + "\n[✔] Done! Press Enter to go back...")

if __name__ == "__main__":
    main()
