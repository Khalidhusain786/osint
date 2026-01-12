import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

# Purana target track karne ke liye (No deletion)
searched_targets = set()

def auto_update():
    """Purana data same rakhte hue patterns update karega"""
    try: os.system("git fetch --all && git reset --hard origin/main")
    except: pass

def start_tor():
    """Tor service auto-start logic - No lines deleted"""
    if os.system("systemctl is-active --quiet tor") != 0:
        print(f"{Fore.CYAN}[!] Starting Tor Service for Anonymous Data Mining...")
        os.system("sudo service tor start")
        time.sleep(3)
    print(f"{Fore.GREEN}[OK] Tor Tunnel: ACTIVE")

def darkweb_power_search(target, report_file):
    """Deep Web aur Darkweb engines (Ahmia, Torch, etc.) - No logic deleted"""
    print(f"{Fore.MAGENTA}[*] Deep Crawling Darkweb Engines & Identity Leaks...")
    engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"https://www.google.com/search?q=site:onion.to+OR+site:onion.pet+%22{target}%22",
        f"https://www.google.com/search?q=%22{target}%22+filetype:pdf+voter+aadhar",
        f"https://www.google.com/search?q=%22{target}%22+password+leaked"
    ]
    try:
        for url in engines:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, timeout=15, headers=headers)
            found_items = re.findall(r'[a-z2-7]{16,56}\.onion|[\w\.-]+@[\w\.-]+\.\w+', res.text)
            if found_items:
                with open(report_file, "a") as f:
                    for item in list(set(found_items)):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.RED}[DEEP-WEB MATCH] {Fore.WHITE}{item}")
                        f.write(f"Discovery: {item}\n")
    except: pass

def run_tool(cmd, name, report_file):
    """Sirf FOUND data screen par dikhayega - Purana logic intact"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Advanced Triggers (Sare purane + naye)
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "aadhar", "voter", "license", "pan", "dob:", "location:", "relative:"]
                if any(x in clean_line.lower() for x in triggers):
                    # Filter for only successful matches
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error", "searching", "trying"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"[{name}] {clean_line}\n")
        process.wait()
    except: pass

def main():
    auto_update()
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - THE OMNI-INTELLIGENCE MONSTER v20.0        ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/ID): ")
    if not target: return
    searched_targets.add(target)
    
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Darkweb Search Thread
    Thread(target=darkweb_power_search, args=(target, report_path)).start()

    # SARE TOOLS (Ek bhi line ya tool delete nahi kiya gaya)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter"),
        (f"holehe {target} --only-used", "Email-Lookup"),
        (f"maigret {target} --timeout 25", "Identity-Mapper"),
        (f"social-analyzer --username {target} --mode fast", "Social-Search"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"phoneinfoga scan -n {target}", "Phone-Intelligence"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"python3 tools/Photon/photon.py -u {target} --wayback", "Web-History"),
        (f"finalrecon --ss --whois --full {target}", "FinalRecon-Full"),
        (f"truecallerpy search --number {target}", "Truecaller-Identity")
    ]

    print(f"{Fore.BLUE}[*] Harvesting Intelligence... ONLY FOUND DATA WILL BE SHOWN:\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Mission Completed. Case File: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
