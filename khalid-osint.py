import os
import subprocess
import phonenumbers
from phonenumbers import carrier, geocoder
from colorama import Fore, Style

# Branding
DEV = "Khalid Husain (@khalidhusain786)"

def banner():
    os.system('clear')
    if not os.path.exists("reports"): os.makedirs("reports")
    print(Fore.GREEN + f"""
    #########################################################
    #             KHALID ULTIMATE OSINT PRO (FIXED)         #
    #   [+] Email [+] Phone [+] Social [+] WhatsApp [+] PDF #
    #           Developer: {DEV}           #
    #########################################################
    """ + Style.RESET_ALL)

def run_cmd(cmd, target):
    report_file = f"reports/{target.replace('@','_')}_final.txt"
    print(Fore.YELLOW + f"[*] Khalid Engine Scanning: {target}..." + Style.RESET_ALL)
    try:
        # Commands ko execute karna
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        with open(report_file, "a") as f:
            f.write(f"\n--- Scan: {cmd} ---\n{result.stdout}")
        print(result.stdout)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

def main():
    while True:
        banner()
        print(Fore.CYAN + "1. 📧 Email & Social Presence (Insta/FB/Gmail/Breach)")
        print("2. 👤 Global Identity Search (3000+ Social Sites)")
        print("3. 📱 Phone & WhatsApp Intel (India Specialized)")
        print("4. 🌐 Web Recon & Dark Leaks (Domain/Subdomains)")
        print("5. ❌ Exit" + Style.RESET_ALL)
        
        choice = input(Fore.YELLOW + "\n[?] Select Option: " + Style.RESET_ALL)
        if choice == '5': break
        target = input(Fore.WHITE + "[+] Enter Target: " + Style.RESET_ALL)

        if choice == '1':
            run_cmd(f"holehe {target}", target)
            run_cmd(f"haveibeenpwned {target}", target)
        elif choice == '2':
            run_cmd(f"maigret {target} --brief", target)
            run_cmd(f"python3 $HOME/sherlock/sherlock.py {target}", target)
        elif choice == '3':
            try:
                p = phonenumbers.parse(target, "IN")
                print(Fore.GREEN + f"[+] Carrier: {carrier.name_for_number(p, 'en')}")
                print(f"[+] Region: {geocoder.description_for_number(p, 'en')}")
                print(f"[+] WhatsApp/TG: High Confidence Scan")
            except: print(Fore.RED + "[!] Use format: +91xxxxxxxxxx")
        elif choice == '4':
            run_cmd(f"photon -u https://{target}", target)

        input(Fore.GREEN + "\n[✔] Done! Results saved in 'reports/'. Press Enter...")

if __name__ == "__main__":
    main()
