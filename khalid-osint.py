import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup

init(autoreset=True)
print_lock = Lock()

# --- TARGET IDENTITY FILTERS (ONLY RESULTS) ---
SURE_HITS = [
    r"[A-Z]{5}[0-9]{4}[A-Z]{1}", # PAN
    r"[A-Z]{3}[0-9]{7}",          # Voter ID
    r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}", # Vehicle RC
    r"(?:\+91|0)?[6-9]\d{9}",     # Indian Phone (Strict)
    r"\b\d{6}\b",                 # Pincode
    r"https?://\S+",              # Links
    r"S/O|D/O|W/O|R/O|Address|Resident" # Relations/Address
]

proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")
    print(f"{Fore.GREEN}[OK] Ghost Tunnel: ACTIVE")

def clean_and_verify(raw_html, target, report_file, source_label):
    """AI logic to purify data and show only matches"""
    try:
        soup = BeautifulSoup(raw_html, 'lxml')
        text = soup.get_text(separator=' ')
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Only process lines mentioning the target or having identity patterns
            if target.lower() in line.lower() or any(re.search(p, line) for p in SURE_HITS[:4]):
                # Final Regex Validation
                for pattern in SURE_HITS:
                    matches = re.findall(pattern, line, re.I)
                    if matches:
                        with print_lock:
                            # Screen par sirf accurate data dikhayega
                            print(f"{Fore.RED}[{source_label}] {Fore.WHITE}{line[:150]}")
                            with open(report_file, "a") as f: 
                                f.write(f"[{source_label}] {line}\n")
                        break # Ek line ke liye ek hi bar save karein
    except: pass

def shadow_crawler_ai(target, report_file):
    """Deep crawling with AI cleaning logic"""
    gateways = [
        f"https://ahmia.fi/search/?q={target}+india+leak",
        f"https://psbdmp.ws/api/search/{target}",
        f"http://juhanurmihxlp77nkq76byv6h6o4ujysoe62clq2u6si7yo76v6pwy6id.onion/search/?q={target}",
        f"https://www.google.com/search?q=site:t.me+OR+site:facebook.com+%22{target}%22"
    ]
    for url in gateways:
        try:
            is_onion = ".onion" in url or "ahmia" in url
            res = requests.get(url, proxies=proxies if is_onion else None, timeout=15, headers=headers)
            clean_and_verify(res.text, target, report_file, "SHADOW-INTEL")
        except: pass

def silent_tool_runner(cmd, name, report_file):
    """Filters tools like Social-Analyzer/Sherlock to show ONLY hits"""
    try:
        process = subprocess.Popen(f"torsocks {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            clean = line.strip()
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
    print(f"{Fore.RED}║   KHALID SHADOW BUREAU - SUPERFAST AI MODE v72.0          ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/PAN): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")
    if os.path.exists(report_path): os.remove(report_path)

    print(f"{Fore.BLUE}[*] Engine Initialized: Extracting Accurate Data (Clean Mode)...\n")

    # Ultra-Fast Parallel Threads
    threads = [
        Thread(target=shadow_crawler_ai, args=(target, report_path)),
        Thread(target=silent_tool_runner, args=(f"social-analyzer --username {target} --mode fast --silent", "Social", report_path)),
        Thread(target=silent_tool_runner, args=(f"sherlock {target} --timeout 15", "Sherlock", report_path)),
        Thread(target=silent_tool_runner, args=(f"maigret {target} --timeout 15", "Maigret", report_path))
    ]

    for t in threads: t.start()
    for t in threads: t.join()

    print(f"\n{Fore.GREEN}[➔] Scan Complete. All Accurate Data Saved: {report_path}")

if __name__ == "__main__":
    main()
