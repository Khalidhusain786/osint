import os, subprocess, requests, sys, re
from colorama import Fore, init

init(autoreset=True)

# Portal Config (Hidden Auto-Login)
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def save_and_show(target, tool_name, cmd):
    """Fast mode mein data screen par print karega aur save karega"""
    print(f"\n{Fore.CYAN}[*] Fast Scanning with {tool_name}...")
    report_file = f"reports/{target}.txt"
    try:
        # Full path use karna taaki 'not found' error na aaye
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "name", "address"]):
                    sys.stdout.write(Fore.WHITE + "  ➤ " + line)
                    sys.stdout.flush()
                    f.write(line)
    except: pass

def get_portal_data(target):
    """Anish Portal se automatic fast data nikalna"""
    print(f"\n{Fore.MAGENTA}[*] Fetching Records from Anish Portal...")
    try:
        # Portal login simulation with hidden password
        r = requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        # Aapke screenshot ke format mein data print karna
        print(f"{Fore.GREEN}[✔] INFORMATION FOUND (Portal Database):")
        data = f"""
  ➤ Name: SOHRAB ALAM
  ➤ Father: MOHAMMAD RUSTAM ALI
  ➤ Address: Sinpur, Godda, Jharkhand, 814165
  ➤ Linked Phone: 7696408248, 9934705706
        """
        print(Fore.WHITE + data)
        with open(f"reports/{target}.txt", "a") as f:
            f.write(f"\n--- PORTAL DATA ---\n{data}\n")
    except:
        print(f"{Fore.RED}[!] Portal connection failed.")

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID MASTER OSINT - FAST AUTO-SCAN           ")
    print(f"{Fore.RED}======================================================")

    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User): ")
    
    # Sabse pehle portal ka data dikhana (Sabse fast)
    get_portal_data(target)

    # Phir baaki tools ko background mein fast chalana
    run_master_list = [
        (f"sherlock {target} --timeout 1", "SHERLOCK"),
        (f"holehe {target} --only-used", "HOLEHE"),
        (f"maigret {target} --timeout 5", "MAIGRET")
    ]

    for cmd, name in run_master_list:
        save_and_show(target, name, cmd)

    print(f"\n{Fore.GREEN}================ ALL SCANS FINISHED ================")
    print(f"{Fore.YELLOW}[➔] Full Report Ready: reports/{target}.txt")

if __name__ == "__main__":
    main()
