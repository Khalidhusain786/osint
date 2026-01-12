import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def auto_update():
    """Script aur Databases ko latest version par update karega"""
    print(f"{Fore.CYAN}[*] Checking for Updates...")
    try:
        # GitHub se latest changes fetch karega
        os.system("git fetch --all && git reset --hard origin/main")
        print(f"{Fore.GREEN}[OK] Script is up to date.")
    except:
        print(f"{Fore.RED}[!] Update failed, skipping...")

def start_tor():
    """Tor service ko automatically check aur start karega"""
    print(f"{Fore.YELLOW}[*] Checking Tor Service...")
    status = os.system("systemctl is-active --quiet tor")
    if status != 0:
        print(f"{Fore.CYAN}[!] Tor is inactive. Starting it now...")
        os.system("sudo service tor start")
        time.sleep(2)
    print(f"{Fore.GREEN}[OK] Tor Service is Active.")

def search_breach_logs(target, report_file):
    """Deep search for leaks in Pastebin & Ahmia"""
    print(f"{Fore.MAGENTA}[*] Searching Deep-Web & Leak Databases...")
    ahmia_url = f"https://ahmia.fi/search/?q={target}"
    try:
        res = requests.get(ahmia_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        leaks = re.findall(r'[a-z2-7]{16,56}\.onion', res.text)
        if leaks:
            with open(report_file, "a") as f:
                for leak in list(set(leaks)):
                    print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                    print(f"{Fore.RED}[BREACH/ONION] {Fore.WHITE}http://{leak}")
                    f.write(f"Darkweb Leak: http://{leak}\n")
    except: pass

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Telegram style 'Found Only' Filter
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "location:"]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    auto_update() # Sabse pehle update check karega
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor() # Tor service start
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - AUTO-UPDATE BREACH ENGINE      ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/User/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    Thread(target=search_breach_logs, args=(target, report_path)).start()

    # Sare powerful tools list
    tools = [
        (f"h8mail -t {target} -q", "H8Mail (Breach DB)"),
        (f"holehe {target} --only-used", "Email-Breach-Check"),
        (f"maigret {target} --timeout 15 --no-recursion", "Deep-ID (Maigret)"),
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"phoneinfoga scan -n {target}", "Phone-Lookup"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock")
    ]

    print(f"{Fore.BLUE}[*] Accessing updated databases & darkweb logs...\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}[➔] Investigation Finished. Check: {report_path}")

if __name__ == "__main__":
    main()
