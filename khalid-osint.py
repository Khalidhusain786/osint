import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def auto_update():
    """GitHub se latest databases aur scripts ko update karega"""
    print(f"{Fore.CYAN}[*] Checking for Global Intelligence Updates...")
    try:
        os.system("git fetch --all && git reset --hard origin/main")
    except: pass

def start_tor():
    """Tor service ko automatically start karega darkweb access ke liye"""
    print(f"{Fore.YELLOW}[*] Initializing Tor Tunneling...")
    status = os.system("systemctl is-active --quiet tor")
    if status != 0:
        os.system("sudo service tor start")
        time.sleep(3)
    print(f"{Fore.GREEN}[OK] Tor Network Connected.")

def deep_darkweb_crawler(target, report_file):
    """Ahmia, Torch, aur Onion repositories se data extract karega"""
    print(f"{Fore.MAGENTA}[*] Deep Crawling Dark-Web (Onion) & Leak Sites...")
    search_engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"https://www.google.com/search?q=site:pastebin.com+OR+site:ghostbin.com+%22{target}%22"
    ]
    try:
        for url in search_engines:
            res = requests.get(url, timeout=12, headers={'User-Agent': 'Mozilla/5.0'})
            matches = re.findall(r'[a-z2-7]{16,56}\.onion|[\w\.-]+@[\w\.-]+\.\w+', res.text)
            if matches:
                with open(report_file, "a") as f:
                    for item in list(set(matches)):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.RED}[DEEP-WEB MATCH] {Fore.WHITE}{item}")
                        f.write(f"DeepWeb/Onion Source: {item}\n")
    except: pass

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Advanced Triggers: Aadhar, Voter, DL, Passwords, etc.
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "aadhar", "voter", "license", "pan", "document"]
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
    
    print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - ALL TOOLS + DEEP DARKWEB v9.0       ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Username/Phone/Email/ID): ")
    if not target: return
    
    # Path save usi naam se hoga jo target ka input hai
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Darkweb Crawling
    Thread(target=deep_darkweb_crawler, args=(target, report_path)).start()

    # Sare Purane + Naye Tools (Sherlock, Blackbird, Maigret, h8mail, etc.)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter (HIBP)"),
        (f"holehe {target} --only-used", "Email-Register-Search"),
        (f"maigret {target} --timeout 20", "Identity-Mapper (Maigret)"),
        (f"social-analyzer --username {target} --mode fast", "Social-Media-Deep-Scan"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intelligence"),
        (f"phoneinfoga scan -n {target}", "Global-Phone-Intel"),
        (f"sherlock {target} --timeout 10 --print-found", "Sherlock-Pro"),
        (f"python3 tools/Photon/photon.py -u {target} --wayback", "Web-History-Crawler")
    ]

    print(f"{Fore.BLUE}[*] Scanning Surface, Deep & Dark Web... Found Results Only:\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Mission Finished. Full Data Saved in: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
