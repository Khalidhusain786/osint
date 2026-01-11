import os
import sys
import subprocess
from colorama import Fore, Style

# Developer: Khalid Husain (@khalidhusain786)

def banner():
    print(Fore.GREEN + """
    #################################################
    #           KHALID OSINT PRO MASTER             #
    #       Developed by: Khalid Husain             #
    #################################################
    """ + Style.RESET_ALL)

def run_cmd(cmd, report_file):
    # Folder check
    if not os.path.exists("reports"):
        os.makedirs("reports")
        
    print(Fore.YELLOW + f"[*] Running: {cmd}" + Style.RESET_ALL)
    try:
        # Result ko terminal aur file dono mein save karega
        output = subprocess.check_output(cmd, shell=True, text=True)
        with open(report_file, "a") as f:
            f.write(output)
        print(output)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)

def main():
    while True:
        banner()
        print("1. 📧 Email Discovery (Holehe + Breach)")
        print("2. 👤 Identity Search (Sherlock + Maigret)")
        print("3. 📱 Phone Scan (Indian Carrier/Region)")
        print("4. 🌐 Website Recon (Amass + Photon)")
        print("5. ❌ Exit")
        
        choice = input(Fore.CYAN + "\n[?] Select Option: " + Style.RESET_ALL)
        if choice == '5': break
        
        target = input("[+] Enter Target: ")
        report_path = f"reports/{target}_report.txt"

        if choice == '1':
            run_cmd(f"holehe {target}", report_path)
            run_cmd(f"haveibeenpwned {target}", report_path)
        elif choice == '2':
            run_cmd(f"maigret {target} --brief", report_path)
            run_cmd(f"python3 ~/sherlock/sherlock.py {target}", report_path)
        elif choice == '3':
            # Phone feature (Simulated for India)
            run_cmd(f"echo 'Phone: {target}\nInfo: Carrier tracking initiated...' ", report_path)
        elif choice == '4':
            run_cmd(f"amass enum -d {target}", report_path)

        print(Fore.GREEN + f"\n[✔] Done! Report: {report_path}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
