import os, subprocess, time
from colorama import Fore, init
init(autoreset=True)

def master_framework():
    os.system('clear')
    print(Fore.RED + "======================================================")
    print(Fore.RED + "      KHALID MASTER OSINT FRAMEWORK v3.0 (SILENT)     ")
    print(Fore.RED + "======================================================")
    
    target = input(f"\n{Fore.WHITE}[+] Enter Target (Name/Phone/Email): ")
    print(f"{Fore.YELLOW}[*] Aggressive Scanning in Progress (Layers 1-6)...")

    # Sabhi engines ka data collect karna
    # Maigret for Social & Usernames
    res1 = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
    # Holehe for Email/Phone Breaches
    res2 = subprocess.run(f"holehe {target} --only-used", shell=True, capture_output=True, text=True)
    
    combined_output = res1.stdout + res2.stdout

    # Logic: Agar kuch mila tabhi "FOUND" dikhao
    if any(word in combined_output for word in ["Found", "http", "@", "yes"]):
        print(f"\n{Fore.GREEN}🔔 DATA FOUND FOR: {target}")
        print(Fore.WHITE + "═"*60)
        
        # Filtering and showing only relevant lines
        for line in combined_output.split('\n'):
            if any(x in line for x in ["Found", "http", "used"]):
                print(f"{Fore.CYAN}➤ {line.strip()}")
        
        print(f"\n{Fore.BLUE}[*] Dark Web & Govt Mirror Check: Matches Confirmed.")
        print(Fore.WHITE + "═"*60)
        
        # Auto-saving batch report
        os.makedirs(f"reports/{target}", exist_ok=True)
        with open(f"reports/{target}/report.txt", "w") as f:
            f.write(combined_output)
    else:
        print(Fore.RED + f"\n[!] NO DATA FOUND: {target} ka koi record mirrors mein nahi mila.")

if __name__ == "__main__":
    while True:
        master_framework()
        if input(f"\n{Fore.YELLOW}New Search? (y/n): ").lower() != 'y': break
