import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup

init(autoreset=True)
print_lock = Lock()

# --- TARGET IDENTITY FILTERS (UPDATED FOR PASSPORT, BANK, ADDRESS) ---
SURE_HITS = {
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "Passport": r"[A-Z][0-9]{7}",                   # Indian Passport pattern
    "Bank_Acc": r"\b[0-9]{9,18}\b",                 # Generic Bank Account (9-18 digits)
    "VoterID": r"[A-Z]{3}[0-9]{7}",
    "Phone": r"(?:\+91|0)?[6-9]\d{9}",
    "Pincode": r"\b\d{6}\b",
    "Address": r"(?i)(Gali\s?No|House\s?No|H\.No|Plot\s?No|Floor|Sector|Ward|Tehsil|District)"
}

proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")
    print(f"{Fore.GREEN}[OK] Ghost Tunnel: ACTIVE")

def clean_and_verify(raw_html, target, report_file, source_label):
    try:
        soup = BeautifulSoup(raw_html, 'lxml')
        for script in soup(["script", "style", "nav", "header", "footer"]): 
            script.decompose()
            
        text = soup.get_text(separator=' ')
        lines = [line.strip() for line in text.split('\n') if target.lower() in line.lower() or any(re.search(p, line) for p in SURE_HITS.values())]

        for line in lines:
            if len(line) < 5: continue
            
            found_ids = []
            for label, pattern in SURE_HITS.items():
                match = re.search(pattern, line)
                if match:
                    # Highlight specific data
                    found_ids.append(f"{Fore.YELLOW}{label}: {match.group()}")

            if found_ids or target.lower() in line.lower():
                output = " | ".join(found_ids) if found_ids else "Text Match"
                with print_lock:
                    print(f"{Fore.RED}[{source_label}-FOUND] {Fore.CYAN}Target: {target} {Fore.WHITE}➔ {output}")
                    # Full line save in report for context
                    with open(report_file, "a") as f: 
                        f.write(f"[{source_label}] {line}\n")
    except: 
        pass

def pdf_document_finder(target, report_file):
    """Resume, PDF aur Documents search with Address/Passport context"""
    dorks = [
        f"https://www.google.com/search?q=site:*.in OR site:*.com filetype:pdf %22{target}%22",
        f"https://www.google.com/search?q=%22{target}%22 + passport OR address filetype:pdf",
        f"https://www.bing.com/search?q=%22{target}%22 + filetype:doc OR filetype:docx"
    ]
    for url in dorks:
        try:
            res = requests.get(url, timeout=10, headers=headers)
            links = re.findall(r'(https?://[^\s<>"]+\.pdf)', res.text)
            for link in links:
                with print_lock:
                    print(f"{Fore.YELLOW}[DOC-LINK] {Fore.WHITE}{link}")
                    with open(report_file, "a") as f: f.write(f"[DOCUMENT] {link}\n")
            clean_and_verify(res.text, target, report_file, "DOC-DATA")
        except: pass

def telegram_dork_engine(target, report_file):
    tg_links = [
        f"https://www.google.com/search?q=site:t.me+%22{target}%22",
        f"https://www.bing.com/search?q=site:t.me+%22{target}%22",
        f"https://yandex.com/search/?text=site:t.me+%22{target}%22",
        f"https://ahmia.fi/search/?q=t.me+{target}"
    ]
    for url in tg_links:
        try:
            is_onion = "ahmia" in url
            res = requests.get(url, proxies=proxies if is_onion else None, timeout=10, headers=headers)
            clean_and_verify(res.text, target, report_file, "TG-DATA")
        except: pass

def shadow_crawler_ai(target, report_file):
    gateways = [
        f"https://ahmia.fi/search/?q={target}+india+leak",
        f"https://psbdmp.ws/api/search/{target}",
        f"https://www.google.com/search?q=site:facebook.com+OR+site:instagram.com+%22{target}%22"
    ]
    for url in gateways:
        try:
            is_onion = "ahmia" in url
            res = requests.get(url, proxies=proxies if is_onion else None, timeout=10, headers=headers)
            clean_and_verify(res.text, target, report_file, "LEAK-DATA")
        except: pass

def silent_tool_runner(cmd, name, report_file):
    try:
        process = subprocess.Popen(f"torsocks {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            clean = line.strip()
            if any(x in clean.lower() for x in ["http", "found", "match:"]):
                if not any(noise in clean.lower() for noise in ["searching", "checking", "trying", "0 results"]):
                    with print_lock:
                        print(f"{Fore.GREEN}[{name.upper()}-HIT] {Fore.WHITE}{clean}")
                        with open(report_file, "a") as f: f.write(f"[{name}] {clean}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID SHADOW BUREAU - TG + ACCURATE MODE v74.0       ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/PAN): ")
    if not target: return
    
    report_path = os.path.abspath(f"reports/{target}.txt")
    if os.path.exists(report_path): os.remove(report_path)
    
    print(f"{Fore.BLUE}[*] Parallel Scanning: Extracting Accurate Matches Only...\n")
    
    threads = [
        Thread(target=pdf_document_finder, args=(target, report_path)),
        Thread(target=telegram_dork_engine, args=(target, report_path)),
        Thread(target=shadow_crawler_ai, args=(target, report_path)),
        Thread(target=silent_tool_runner, args=(f"social-analyzer --username {target} --mode fast --silent", "Social", report_path)),
        Thread(target=silent_tool_runner, args=(f"sherlock {target} --timeout 10", "Sherlock", report_path)),
        Thread(target=silent_tool_runner, args=(f"maigret {target} --timeout 10", "Maigret", report_path))
    ]
    
    for t in threads: t.start()
    for t in threads: t.join()
    
    print(f"\n{Fore.GREEN}[➔] Scan Complete. Accurate Matches Saved: {report_path}")

if __name__ == "__main__":
    main()
