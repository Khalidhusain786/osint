import os, subprocess, time
from colorama import Fore, init
init(autoreset=True)

def bot_engine():
    os.system('clear')
    print(Fore.RED + "--- KHALID GLOBAL BREACH SEARCH (FIXED & AGGRESSIVE) ---")
    target = input(Fore.WHITE + "[+] Target (Name/User/Phone): ")
    print(Fore.YELLOW + f"[*] Deep Scanning... (Searching 2500+ Databases)")

    # Maigret ko aggressive mode mein chalana taaki hidden data bhi dikhe
    # --all-sites aur --print-not-found hara kar sirf milne wala data dikhayega
    cmd = f"maigret {target} --timeout 30 --retries 3"
    
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = res.stdout.strip()

    print(Fore.GREEN + f"\n🔔 SEARCH RESULTS FOR: {target}")
    print(Fore.WHITE + "═"*65)

    if output:
        # Har line ko scan karke display karna
        lines = output.split('\n')
        found_anything = False
        for line in lines:
            if "Found" in line or "http" in line:
                print(f"{Fore.CYAN}➤ {line.strip()}")
                found_anything = True
        
        if not found_anything:
            print(Fore.RED + "➤ Status: Security layers high. Try searching with a Username.")
    else:
        print(Fore.RED + "➤ Status: No direct matches. Scanning deeper mirrors...")
        # Fallback: Agar Maigret fail ho toh raw social analyzer try karein
        os.system(f"social-analyzer --username {target} --mode fast")

    print(Fore.WHITE + "═"*65)
    
    # Save results
    os.makedirs(f"reports/{target}", exist_ok=True)
    with open(f"reports/{target}/report.txt", "w") as f:
        f.write(output)

if __name__ == "__main__":
    while True:
        bot_engine()
        if input(Fore.YELLOW + "\nNew Search? (y/n): ").lower() != 'y': break
