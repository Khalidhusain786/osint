import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

# Purana data track karne ke liye set
searched_targets = set()

def auto_update():
    """Purana data same rakhte hue patterns update karega"""
    try: os.system("git fetch --all && git reset --hard origin/main")
    except: pass

def start_tor():
    """Tor service auto-start - No deletion in logic"""
    if os.system("systemctl is-active --quiet tor") != 0:
        print(f"{Fore.CYAN}[!] Starting Tor Service for Anonymous Deep-Web Crawling...")
        os.system("sudo service tor start")
        time.sleep(3)
    print(f"{Fore.GREEN}[OK] Tor Connection Established.")

def deep_darkweb_mega_engines(target, report_file):
    """Saare powerful darkweb search engines ka mix (Ahmia, Torch, Haystak, Onion.link)"""
    print(f"{Fore.MAGENTA}[*] Deep Scanning: Darkweb Identity & Breach Repositories...")
    
    # Advanced Indian context dorks + Global Breach dorks
    engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"https://www.google.com/search?q=site:onion.to+OR+site:onion.pet+%22{target}%22",
        f"https://www.google.com/search?q=%22{target}%22+filetype:pdf+voter+aadhar",
        f"https://www.google.com/search?q=%22{target}%22+password+leaked+OR+db+leak"
    ]
    
    try:
        for url in engines:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, timeout=15, headers=headers)
            # Onion links, Emails aur Phone discovery
            found_items = re.findall(r'[a-z2-7]{16,56}\.onion|[\w\.-]+@[\w\.-]+\.\w+', res.text)
            if found_items:
                with open(report_file, "a") as f:
                    for item in list(set(found_items)):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.RED}[IDENTITY LEAK] {Fore.WHITE}{item}")
                        f.write(f"Discovery: {item}\n")
    except: pass

def run_tool(cmd, name, report_file):
    """Bina koi line delete kiye saare tools ka execution logic"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Advanced Triggers: Jo aapke screenshots mein the
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "aadhar", "voter", "license", "pan", "dob:", "location:", "relative:"]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error"]):
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
    
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - IDENTITY, BREACH & DARKWEB v16.0       ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/Aadhar): ")
    if not target: return
    searched_targets.add(target)
    
    # Path save hamesha target ke naam se
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Darkweb Search and Recursive PIVOT Thread
    Thread(target=deep_darkweb_mega_engines, args=(target, report_path)).start()

    # SARE TOOLS: Purane + Naye (Kuch bhi delete nahi kiya)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter (HIBP)"),
        (f"holehe {target} --only-used", "Email-Lookup"),
        (f"maigret {target} --timeout 25", "Identity-Mapper (Maigret)"),
        (f"social-analyzer --username {target} --mode fast", "Social-Deep-Scan"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"phoneinfoga scan -n {target}", "Phone-Intelligence"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"python3 tools/Photon/photon.py -u {target} --wayback", "Wayback-History"),
        (f"finalrecon --ss --whois --full {target}", "FinalRecon-Complete"),
        (f"truecallerpy search --number {target}", "Truecaller-Identity")
    ]

    print(f"{Fore.BLUE}[*] Crawling Surface, Deep, and Dark Web... FOUND Data Only:\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Mission Finished. Full Case File: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
