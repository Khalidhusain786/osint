import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

# Forensic & Reporting (Legacy All Preserved)
try: import pdfkit
except: pass

init(autoreset=True)
all_raw_findings = [] 

# TOR PROXY CONFIGURATION
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# --- DEEP DARKNET ENGINES (NEW v54) ---

def private_forum_crawler(target, report_file):
    """
    V54: Private Tor Forum & Directory Scraper.
    Targets: Dark.fail mirrors, Dread, and Hidden Forums.
    """
    print(f"{Fore.MAGENTA}[*] Deep Crawling: Private Tor Forums & Dark.fail Mirrors...")
    
    # Private Directories & Forum Search Aggregators
    dark_nodes = [
        f"https://dark.fail/", # Directory monitoring
        f"http://duckduckgogg42xjoc72x3sja7o784uuy6qzts6ee7tbb9z473aad.onion/?q={target}", # DDG Onion
        f"http://haystak5njsu5hk.onion/search.php?q={target}", # Haystak Deep Search
        f"http://v6v6v6v6v6v6v6v6.onion/search?q={target}", # Private Forum Indexer
        f"http://xmh57jrknzkhv6y3ls3ubv6iwixcebcms7u6at76baqx3ara6o86f2ad.onion/search?q={target}" # Torch Mirror
    ]

    for url in dark_nodes:
        try:
            # Using SOCKS5h for Onion sites
            res = requests.get(url, proxies=proxies, timeout=25)
            # Extracting potential forum threads or leak posts
            leaks = re.findall(r'([a-z2-7]{16,56}\.onion/post/\d+)', res.text)
            if leaks:
                with open(report_file, "a") as f:
                    for leak in list(set(leaks)):
                        result = f"Private Forum Post: http://{leak}"
                        print(f"{Fore.RED}[FORUM-LEAK] {Fore.WHITE}{result}")
                        f.write(f"[DARK-FORUM] {result}\n")
                        all_raw_findings.append(result)
        except: pass

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start")
        time.sleep(2)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def identity_government_engine(target, report_file):
    """V53: Verified Identity Engine (Intact)"""
    patterns = {"Aadhar": r'\b\d{4}\s\d{4}\s\d{4}\b', "PAN": r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'}
    try:
        res = requests.get(f"https://www.google.com/search?q={target}+Aadhar", timeout=10)
        for label, pattern in patterns.items():
            matches = re.findall(pattern, res.text)
            for m in list(set(matches)):
                print(f"{Fore.GREEN}[VERIFIED-ID] {Fore.WHITE}{label}: {m}")
                all_raw_findings.append(f"{label}: {m}")
    except: pass

def run_tool_strict_found(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                if not clean_line: continue
                f.write(f"{clean_line}\n")
                if any(x in clean_line.lower() for x in ["password:", "breach:", "location:"]):
                    print(f"{Fore.GREEN}[FOUND] {Fore.YELLOW}{name}: {Fore.WHITE}{clean_line}")
                    all_raw_findings.append(clean_line)
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - PRIVATE FORUM & DARK-CRAWLER v54.0       ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Username/Email/ID): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start Background Engines
    Thread(target=private_forum_crawler, args=(target, report_path)).start()
    Thread(target=identity_government_engine, args=(target, report_path)).start()

    # LEGACY TOOLS
    tools = [
        (f"h8mail -t {target} -q", "Breach-Search"),
        (f"python3 -m blackbird -u {target}", "Handle-Intel"),
        (f"maigret {target} --timeout 20", "Social-Deep-Scan")
    ]

    print(f"{Fore.BLUE}[*] Hit Haystak, DDG Onion, & Private Forum Nodes...\n")
    threads = [Thread(target=run_tool_strict_found, args=(cmd, name, report_path)) for cmd, name in tools]
    for t in threads: t.start()
    for t in threads: t.join()

    print(f"\n{Fore.GREEN}[➔] Deep Scan Complete! Check Log: {report_path}")

if __name__ == "__main__":
    main()
