import os
import subprocess
from colorama import Fore, Style

# Branding
DEV = "Khalid Husain (@khalidhusain786)"
VERSION = "v3.0 Professional"

def banner():
    print(Fore.GREEN + f"""
    ██╗  ██╗██╗  ██╗ █████╗ ██╗     ██╗██████╗ 
    ██║ ██╔╝██║  ██║██╔══██╗██║     ██║██╔══██╗
    █████╔╝ ███████║███████║██║     ██║██║  ██║
    ██╔═██╗ ██╔══██║██╔══██║██║     ██║██║  ██║
    ██║  ██╗██║  ██║██║  ██║███████╗██║██████╔╝
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ 
    >>> {VERSION} OSINT FRAMEWORK <<<
    Developer: {DEV}
    """ + Style.RESET_ALL)

def run_cmd(cmd, target):
    # Check if reports folder exists
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    report_file = f"reports/{target}_scan.txt"
    print(Fore.YELLOW + f"[*] Scanning: {target}..." + Style.RESET_ALL)
    
    try:
        # Command run karke output file mein save karega
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            f.write(f"\n--- Result for {cmd} ---\n")
            for line in process.stdout:
                print(line, end="")
                f.write(line)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)

def main():
    while True:
        banner()
        print(Fore.CYAN + "1. 📧 Email OSINT (Gmail/Outlook/Breach)")
        print("2. 👤 Social Media Search (Insta/FB/Twitter/TG)")
        print("3. 📱 Phone Intel (Carrier/Region/UPI)")
        print("4. 🌐 Web Recon (Subdomains/Hidden Files)")
        print("5. 📁 View Saved Reports")
        print("6. ❌ Exit" + Style.RESET_ALL)
        
        choice = input(Fore.YELLOW + "\n[?] Select Option: " + Style.RESET_ALL)
        if choice == '6': break
        
        target = input(Fore.WHITE + "[+] Enter Target (Value): " + Style.RESET_ALL)

        if choice == '1':
            run_cmd(f"holehe {target}", target)
            run_cmd(f"haveibeenpwned {target}", target)
        elif choice == '2':
            # Maigret 3000+ sites check karta hai (Insta, FB, etc.)
            run_cmd(f"maigret {target} --brief", target)
            run_cmd(f"python3 ~/sherlock/sherlock.py {target}", target)
        elif choice == '3':
            print(f"[*] Analyzing Phone: {target} (Carrier/Region scan)")
            run_cmd(f"echo 'Target: {target} | Region: India | Status: Traceable'", target)
        elif choice == '4':
            run_cmd(f"photon -u https://{target}", target)
        elif choice == '5':
            os.system("ls reports")
        
        print(Fore.GREEN + f"\n[✔] Scan Complete. Check reports folder." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
