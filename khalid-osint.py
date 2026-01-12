import os, subprocess, sys, requests, re
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def search_breach_logs(target, report_file):
    """Deep search for leaks in Pastebin, Ahmia, and public archives"""
    print(f"{Fore.MAGENTA}[*] Checking Data-Breach Logs & Darkweb Archives...")
    
    # Ahmia (Darkweb Index) aur Google Dorks ka combination
    search_engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"https://www.google.com/search?q=site:pastebin.com+%22{target}%22"
    ]
    
    try:
        for url in search_engines:
            res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            # Link extraction for onion and leaks
            leaks = re.findall(r'[a-z2-7]{16,56}\.onion|pastebin\.com/[a-zA-Z0-9]+', res.text)
            if leaks:
                with open(report_file, "a") as f:
                    for leak in list(set(leaks)):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.RED}[DATA LEAK] {Fore.WHITE}{leak}")
                        f.write(f"Leak Source: {leak}\n")
    except: pass

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # TELEGRAM BOT STYLE FILTER: Sirf 'Found' data dikhayega
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "location:"]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error", "searching"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║     KHALID OSINT - BREACH & DARKWEB BOT v6.0     ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/User/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Breach Logs Search in Background
    Thread(target=search_breach_logs, args=(target, report_path)).start()

    # Sabse Powerful Breach & OSINT Tools
    tools = [
        (f"h8mail -t {target} -q", "H8Mail (Breach Search)"),
        (f"holehe {target} --only-used", "Email-Breach-Check"),
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"maigret {target} --timeout 15 --no-recursion", "Deep-ID (Maigret)"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intelligence"),
        (f"phoneinfoga scan -n {target}", "Phone-Lookup"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock")
    ]

    print(f"{Fore.BLUE}[*] Fetching data from 500+ Breach Databases...\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}[➔] Scan Complete. Results Saved in: {report_path}")

if __name__ == "__main__":
    main()
