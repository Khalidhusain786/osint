import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread, Lock

init(autoreset=True)
print_lock = Lock()

# --- TARGET IDENTITY FILTERS (ONLY RESULTS) ---
SURE_HITS = [
    r"[A-Z]{5}[0-9]{4}[A-Z]{1}", # PAN
    r"[A-Z]{3}[0-9]{7}",          # Voter ID
    r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}", # Vehicle RC
    r"(?:\+91|0)?[6-9]\d{9}",     # Indian Phone
    r"\b\d{6}\b",                 # Pincode
    r"https?://\S+",              # Links
    r"S/O|D/O|W/O|R/O"            # Relations/Address
]

proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")
    print(f"{Fore.GREEN}[OK] Ghost Tunnel: ACTIVE")

def shadow_telegram_crawler(target, report_file):
    """
    Bina API ke Telegram Crawler (Using Web-Gateways)
    Dumps aur leaked files dhoondhne ke liye
    """
    # Telegram web mirrors and search aggregators
    gateways = [
        f"https://ahmia.fi/search/?q={target}+telegram+leak",
        f"https://www.google.com/search?q=site:t.me+OR+site:tgstat.com+%22{target}%22"
    ]
    for url in gateways:
        try:
            # Note: Tor proxy used for darkweb search
            res = requests.get(url, proxies=proxies if "ahmia" in url else None, timeout=15)
            # AI Check for specific data
            for pattern in SURE_HITS:
                matches = re.findall(pattern, res.text)
                for m in list(set(matches))[:5]:
                    with print_lock:
                        print(f"{Fore.RED}[SHADOW-INTEL] {Fore.WHITE}{m}")
                        with open(report_file, "a") as f: f.write(f"[SHADOW] {m}\n")
        except: pass

def deep_data_extractor(target, report_file):
    """Deep scan for PAN/Voter/Address from leak repositories"""
    mirrors = [
        f"http://juhanurmihxlp77nkq76byv6h6o4ujysoe62clq2u6si7yo76v6pwy6id.onion/search/?q={target}",
        f"https://psbdmp.ws/api/search/{target}"
    ]
    for m_url in mirrors:
        try:
            res = requests.get(m_url, proxies=proxies, timeout=20)
            lines = res.text.split('\n')
            for line in lines:
                if target.lower() in line.lower():
                    # Check if line contains identity numbers or address
                    if any(re.search(p, line) for p in SURE_HITS):
                        with print_lock:
                            print(f"{Fore.YELLOW}[FOUND-DATA] {Fore.WHITE}{line.strip()}")
                            with open(report_file, "a") as f: f.write(f"[DATA] {line.strip()}\n")
        except: pass

def silent_tool_runner(cmd, name, report_file):
    """Filters tools like Social-Analyzer/Sherlock to show ONLY hits"""
    try:
        process = subprocess.Popen(f"torsocks {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            clean = line.strip()
            # AI Filtering: No "Searching..." noise
            if any(x in clean.lower() for x in ["http", "found", "match", "@"]):
                if not any(noise in clean.lower() for noise in ["searching", "checking", "trying", "0 results"]):
                    with print_lock:
                        print(f"{Fore.GREEN}[{name.upper()}] {Fore.WHITE}{clean}")
                        with open(report_file, "a") as f: f.write(f"[{name}] {clean}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║   KHALID SHADOW BUREAU - ULTIMATE SURVEILLANCE v71.0       ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/PAN): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")
    if os.path.exists(report_path): os.remove(report_path)

    print(f"{Fore.BLUE}[*] AI Multi-Threading Engine: Extraction in Progress (Silent Mode)...\n")

    # High-Speed Parallel Execution
    threads = [
        Thread(target=shadow_telegram_crawler, args=(target, report_path)),
        Thread(target=deep_data_extractor, args=(target, report_path)),
        Thread(target=silent_tool_runner, args=(f"social-analyzer --username {target} --mode fast --silent", "Social", report_path)),
        Thread(target=silent_tool_runner, args=(f"sherlock {target} --timeout 10", "Sherlock", report_path))
    ]

    for t in threads: t.start()
    for t in threads: t.join()

    print(f"\n{Fore.GREEN}[➔] Intelligence Gathered. Report Saved: {report_path}")

if __name__ == "__main__":
    main()
