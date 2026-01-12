import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def auto_update():
    """GitHub se latest databases aur tools update karega"""
    print(f"{Fore.CYAN}[*] Checking for Advanced Updates...")
    try:
        os.system("git fetch --all && git reset --hard origin/main")
        print(f"{Fore.GREEN}[OK] All Advanced Modules are Up-to-Date.")
    except: pass

def start_tor():
    """Tor service ko automatically start karega darkweb access ke liye"""
    print(f"{Fore.YELLOW}[*] Initializing Tor Proxy for Darkweb Access...")
    status = os.path.exists("/var/run/tor/tor.pid") or os.system("systemctl is-active --quiet tor") == 0
    if not status:
        os.system("sudo service tor start")
        time.sleep(3)
    print(f"{Fore.GREEN}[OK] Tor Service is Tunneling.")

def deep_darkweb_search(target, report_file):
    """Ahmia, Torch, aur Haystak dorks ka use karke deep/dark web scan"""
    print(f"{Fore.MAGENTA}[*] Deep Scanning Darkweb & Document Leaks (Aadhar/Voter/DL)...")
    
    # Advanced Dorks for Identity Leaks
    search_engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"https://www.google.com/search?q=site:pastebin.com+OR+site:ghostbin.com+%22{target}%22",
        f"https://www.google.com/search?q=%22{target}%22+filetype:sql+OR+filetype:csv+leak"
    ]
    
    try:
        for url in search_engines:
            res = requests.get(url, timeout=12, headers={'User-Agent': 'Mozilla/5.0'})
            # Onion links aur sensitive documents ke liye regex
            matches = re.findall(r'[a-z2-7]{16,56}\.onion|[\w\.-]+@[\w\.-]+\.\w+', res.text)
            if matches:
                with open(report_file, "a") as f:
                    for item in list(set(matches)):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.RED}[LEAK FOUND] {Fore.WHITE}{item}")
                        f.write(f"Identity Leak Source: {item}\n")
    except: pass

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Advanced Triggers: Aadhar, Voter ID, Password, Phone etc.
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "aadhar", "voter", "license", "fb.com", "instagram"]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    auto_update()
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - ADVANCED IDENTITY & BREACH v8.0    ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (User/Email/Phone/ID): ")
    if not target: return
    
    # Path save usi naam se hoga jo target ka naam hai
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Darkweb Search background mein
    Thread(target=deep_darkweb_search, args=(target, report_path)).start()

    # Sabse Advanced GitHub Tools ki List
    tools = [
        (f"h8mail -t {target} -q", "Breach-Search (HIBP/Leaks)"),
        (f"holehe {target} --only-used", "Email-Register-Check"),
        (f"maigret {target} --timeout 20 --no-recursion", "Identity-Mapper (Maigret)"),
        (f"social-analyzer --username {target} --mode fast", "Social-Media-Deep-Scan"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intelligence"),
        (f"phoneinfoga scan -n {target}", "Global-Phone-Intelligence"),
        (f"sherlock {target} --timeout 8 --print-found", "Sherlock-Pro"),
        (f"python3 tools/Photon/photon.py -u {target} --wayback", "Web-History-Crawler")
    ]

    print(f"{Fore.BLUE}[*] Accessing Global Breach Databases & Onion Nodes...\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}[➔] Investigation Complete. Report Saved as: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
