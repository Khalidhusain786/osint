import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

# No Deletion Policy: All historical tracking intact
searched_targets = set()

def auto_update():
    """Purana data same rakhte hue patterns update karega"""
    try: os.system("git fetch --all && git reset --hard origin/main")
    except: pass

def start_tor():
    """Tor service auto-pilot - All versions' logic combined"""
    if os.system("systemctl is-active --quiet tor") != 0:
        print(f"{Fore.CYAN}[!] Activating Tor Tunnel for Deep/Dark Web Crawling...")
        os.system("sudo service tor start")
        time.sleep(3)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def deep_darkweb_mega_engines(target, report_file):
    """V1 to V27: All Darkweb & Deep Dorking logic merged"""
    engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"https://www.google.com/search?q=site:onion.to+OR+site:onion.pet+%22{target}%22",
        f"https://www.google.com/search?q=%22{target}%22+filetype:pdf+voter+aadhar",
        f"https://www.google.com/search?q=%22{target}%22+password+leaked+OR+db+leak",
        f"https://www.google.com/search?q=site:gov.in+OR+site:nic.in+%22{target}%22",
        f"https://www.google.com/search?q=site:linkedin.com/in/+%22{target}%22"
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
                        print(f"{Fore.RED}[DEEP-DISCOVERY] {Fore.WHITE}{item}")
                        f.write(f"Discovery: {item}\n")
    except: pass

def run_tool(cmd, name, report_file):
    """Sirf FOUND data screen par dikhayega - All triggers from all previous versions added"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Ultimate Triggers List (Bina kuch chhode)
                triggers = [
                    "http", "found", "[+]", "password:", "address:", "father", "name:", "aadhar", 
                    "voter", "license", "pan", "dob:", "location:", "relative:", "job:", "company:", 
                    "title:", "court:", "case:", "employee:", "gps:", "latitude:", "longitude:"
                ]
                if any(x in clean_line.lower() for x in triggers):
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
    print(f"{Fore.RED}║    KHALID OSINT - THE OMNI-RECURSIVE FINAL v28.0            ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/ID): ")
    if not target: return
    searched_targets.add(target)
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start Background Intelligence Threads
    Thread(target=deep_darkweb_mega_engines, args=(target, report_path)).start()

    # ALL TOOLS RESTORED: Sherlock, Maigret, Blackbird, Photon, H8mail, Truecaller, etc.
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

    print(f"{Fore.BLUE}[*] Crawling All Intelligence Layers... SHOWING FOUND DATA ONLY:\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Investigation Complete. Case File: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
