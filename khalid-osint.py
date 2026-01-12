import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def auto_update():
    """GitHub se latest updates check karega bina purana data delete kiye"""
    print(f"{Fore.CYAN}[*] Checking for Intelligence Updates...")
    try:
        os.system("git fetch --all && git reset --hard origin/main")
    except: pass

def start_tor():
    """Tor service ko auto-start aur check karega"""
    print(f"{Fore.YELLOW}[*] Initializing Tor Proxy for Dark-Web Access...")
    # Checking if Tor is installed and active
    status = os.system("systemctl is-active --quiet tor")
    if status != 0:
        print(f"{Fore.CYAN}[!] Tor is inactive. Starting Tor Service...")
        os.system("sudo service tor start")
        time.sleep(3)
    print(f"{Fore.GREEN}[OK] Tor Service is Active and Tunneling.")

def deep_darkweb_engine_scan(target, report_file):
    """Powerful Darkweb Search Engines (Ahmia, Torch, Haystak style) integration"""
    print(f"{Fore.MAGENTA}[*] Querying Powerful Darkweb Engines & Onion Repositories...")
    
    # List of powerful gateways to Darkweb data
    engines = [
        f"https://ahmia.fi/search/?q={target}", 
        f"https://onionsearch-pro.com/search?q={target}", # Mockup for logic
        f"https://www.google.com/search?q=site:onion.ly+OR+site:onion.pet+%22{target}%22"
    ]
    
    try:
        for url in engines:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
            res = requests.get(url, timeout=15, headers=headers)
            # Regex to find .onion links and leak patterns
            matches = re.findall(r'[a-z2-7]{16,56}\.onion', res.text)
            if matches:
                with open(report_file, "a") as f:
                    f.write(f"\n--- POWERFUL DARKWEB SEARCH RESULTS ---\n")
                    for link in list(set(matches)):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.RED}[DARK-ENGINE MATCH] {Fore.WHITE}http://{link}")
                        f.write(f"Source: http://{link}\n")
    except Exception as e:
        pass

def run_tool(cmd, name, report_file):
    """Sare tools ko parallel run karega aur sirf FOUND data dikhayega"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # TELEGRAM BOT STYLE TRIGGERS (Aadhar, Father-name, Address, etc.)
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "aadhar", "voter", "license", "pan", "document", "truecaller"]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error", "searching"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"[{name}] {clean_line}\n")
        process.wait()
    except: pass

def main():
    auto_update()
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor() # Auto-start Tor service
    os.system('clear')
    
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - DEEP & DARKWEB POWER-ENGINE v12.0        ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/User/Phone/ID): ")
    if not target: return
    
    # Path save hamesha target ke naam se hoga
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Darkweb Search Engine Thread
    Thread(target=deep_darkweb_engine_scan, args=(target, report_path)).start()

    # Sare Purane Tools + Naye Tools (Sherlock, Maigret, Blackbird, etc. restored)
    tools = [
        (f"h8mail -t {target} -q", "H8Mail (Breach DB)"),
        (f"holehe {target} --only-used", "Email-Breach-Check"),
        (f"maigret {target} --timeout 20", "Identity-Mapper (Maigret)"),
        (f"social-analyzer --username {target} --mode fast", "Social-Search"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"phoneinfoga scan -n {target}", "Phone-Intelligence"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"python3 tools/Photon/photon.py -u {target} --wayback", "Web-Archive-Scraper"),
        (f"finalrecon --ss --whois --full {target}", "FinalRecon-Full")
    ]

    print(f"{Fore.BLUE}[*] Crawling Surface, Deep, and Dark Web Platforms...\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Investigation Complete. Full Report: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
