import os, subprocess, requests, time
from colorama import Fore, init

init(autoreset=True)

# Portal Config (Hidden)
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def save_and_display(target, tool_name, cmd):
    """Data ko screen par dikhane aur file mein save karne ke liye"""
    print(f"\n{Fore.CYAN}[*] Searching with {tool_name}...")
    report_file = f"reports/{target}.txt"
    
    try:
        # Tool execution
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        
        if len(output.strip()) > 20:
            # Screen Par Dikhana
            print(f"{Fore.GREEN}[✔] {tool_name} Results:")
            print(Fore.WHITE + output)
            
            # File Mein Save Karna
            with open(report_file, "a") as f:
                f.write(f"\n{'='*30}\nTOOL: {tool_name}\n{'='*30}\n")
                f.write(output + "\n")
            return True
    except:
        pass
    return False

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID ULTIMATE ALL-IN-ONE OSINT (V9.0)        ")
    print(f"{Fore.RED}======================================================")

    # Silent Portal Unlock
    try:
        requests.post(P_URL, data={'password': P_KEY}, timeout=5)
        print(f"{Fore.GREEN}[✔] PORTAL ACCESS GRANTED (HIDDEN MODE)")
    except: pass

    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Username/Email/Phone): ")
    print(f"{Fore.BLUE}[*] Deep Scan Shuru... Report 'reports/{target}.txt' mein save hogi.\n")

    # --- ALL TOOLS EXECUTION ---
    
    # 1. Sherlock (Social Media)
    save_and_display(target, "SHERLOCK", f"sherlock {target} --timeout 1 --print-found")
    
    # 2. Holehe (Email OSINT)
    save_and_display(target, "HOLEHE", f"holehe {target} --only-used")
    
    # 3. Maigret (Deep Web Search)
    save_and_display(target, "MAIGRET", f"maigret {target} --timeout 10")

    # 4. Google Dorks (Phone/Name)
    dork_link = f"https://www.google.com/search?q=site:*.in+\"{target}\""
    print(f"\n{Fore.GREEN}[✔] GOOGLE DORK LINK GENERATED:")
    print(f"{Fore.WHITE}  ➤ {dork_link}")
    with open(f"reports/{target}.txt", "a") as f:
        f.write(f"\nGoogle Dork: {dork_link}\n")

    print(f"\n{Fore.CYAN}================ SCAN COMPLETE ================")
    print(f"{Fore.YELLOW}Total data saved in: reports/{target}.txt")

if __name__ == "__main__":
    main()
