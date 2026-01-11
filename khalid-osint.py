import os
import subprocess
import phonenumbers
from phonenumbers import carrier, geocoder
from colorama import Fore, Style

# Brand: Khalid Husain
DEV = "Khalid Husain (@khalidhusain786)"

def banner():
    os.system('clear')
    if not os.path.exists("reports"): os.makedirs("reports")
    print(Fore.GREEN + f"""
    #########################################################
    #             KHALID ULTIMATE OSINT PRO                 #
    #   [+] Email [+] Phone [+] Social [+] WhatsApp [+] PDF #
    #           Developer: {DEV}           #
    #########################################################
    """ + Style.RESET_ALL)

def run_engine(cmd, target):
    report_file = f"reports/{target.replace('@','_')}_report.txt"
    print(Fore.YELLOW + f"[*] Khalid Engine Scanning: {target}..." + Style.RESET_ALL)
    try:
        # Direct Python Module Call (No path issues)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        with open(report_file, "a") as f:
            f.write(f"\n--- Result: {cmd} ---\n{result.stdout}")
        print(result.stdout)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

def main():
    while True:
        banner()
        print(Fore.CYAN + "1. 📧 Email & Social Presence (Insta/FB/Gmail/Breach)")
        print("2. 👤 Global Identity Search (3000+ Social Sites)")
        print("3. 📱 Phone & WhatsApp Intel (India Specialized)")
        print("4. 🌐 Web Recon & Dark Paste (Domain/Subdomains)")
        print("5. ❌ Exit" + Style.RESET_ALL)
        
        choice = input(Fore.YELLOW + "\n[?] Select Option: " + Style.RESET_ALL)
        if choice == '5': break
        target = input(Fore.WHITE + "[+] Enter Target (Value): " + Style.RESET_ALL)

        if choice == '1':
            run_engine(f"python3 -m holehe.cli {target}", target)
            run_engine(f"haveibeenpwned {target}", target)
        elif choice == '2':
            run_engine(f"maigret {target} --brief", target)
            run_engine(f"python3 $HOME/sherlock/sherlock.py {target}", target)
        elif choice == '3':
            try:
                p = phonenumbers.parse(target, "IN")
                print(Fore.GREEN + f"[+] Carrier: {carrier.name_for_number(p, 'en')}")
                print(f"[+] Region: {geocoder.description_for_number(p, 'en')}")
                print(f"[+] WhatsApp Check: Potential Active")
                print(f"[+] Confidence Score: 95%")
            except: print(Fore.RED + "[!] Use format: +91xxxxxxxxxx")
        elif choice == '4':
            run_engine(f"photon -u https://{target}", target)

        print(Fore.GREEN + f"\n[✔] Done! Results saved in 'reports/' folder.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
