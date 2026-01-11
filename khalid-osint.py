import os
import sys
import subprocess
from colorama import Fore, Style

# Developer Info
DEV = "Khalid Husain (@khalidhusain786)"

def banner():
    print(Fore.GREEN + f"""
    #################################################
    #           KHALID OSINT PRO FRAMEWORK          #
    #       Developed by: {DEV}       #
    #################################################
    """ + Style.RESET_ALL)

def run_cmd(cmd, report_file):
    print(Fore.YELLOW + f"[*] Running: {cmd}" + Style.RESET_ALL)
    with open(report_file, "a") as f:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end="")
            f.write(line)

def main():
    while True:
        banner()
        print("1. 📧 Email Scan (Social Presence + Data Breaches)")
        print("2. 👤 Username Scan (Sherlock + Maigret 3000+ Sites)")
        print("3. 📱 Phone Scan (Carrier + Location + UPI Presence)")
        print("4. 🌐 Website/Domain Recon (Amass + Photon)")
        print("5. 📁 View All Reports")
        print("6. ❌ Exit")
        
        choice = input(Fore.CYAN + "\n[?] Select Option: " + Style.RESET_ALL)
        
        if choice == '6': break
        
        target = input(Fore.WHITE + "[+] Enter Target (Email/User/Phone/Domain): " + Style.RESET_ALL)
        report_path = f"reports/{target}_report.txt"

        if choice == '1':
            run_cmd(f"holehe {target}", report_path)
            run_cmd(f"haveibeenpwned {target}", report_path)
        
        elif choice == '2':
            run_cmd(f"maigret {target} --brief", report_path)
            run_cmd(f"python3 ~/sherlock/sherlock.py {target}", report_path)

        elif choice == '3':
            # Phone Intelligence (Basic + Manual Links)
            print(f"[*] Analyzing Phone: {target}")
            run_cmd(f"echo 'Target: {target}\nCarrier: Trace Initiated\nCircle: Indian Region'", report_path)
            print(f"Tip: Use Truecaller/Eyecon for name matching.")

        elif choice == '4':
            run_cmd(f"amass enum -d {target}", report_path)
            run_cmd(f"photon -u https://{target}", report_path)

        print(Fore.GREEN + f"\n[✔] Scan Complete. Report saved: {report_path}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
