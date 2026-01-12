import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

init(autoreset=True)
print_lock = Lock()

# --- TARGET IDENTITY FILTERS (ADVANCED PATTERNS) ---
SURE_HITS = {
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "Aadhaar": r"\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b",
    "Passport": r"[A-Z][0-9]{7}",
    "Bank_Acc": r"\b[0-9]{9,18}\b",
    "VoterID": r"[A-Z]{3}[0-9]{7}",
    "Phone": r"(?:\+91|0)?[6-9]\d{9}",
    "Pincode": r"\b\d{6}\b",
    "Vehicle": r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}",
    "Address": r"(?i)(Gali\s?No|H\.No|Plot|Sector|Ward|Tehsil|District|PIN:)",
    "Relations": r"(?i)(Father|Mother|W/O|S/O|D/O|Relative|Alternative|Nominee)",
    "Location": r"(?i)(Village|City|State|Country|Map|Lat|Long)"
}

def get_onion_session():
    session = requests.Session()
    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    session.proxies.update(proxies)
    retry_strategy = Retry(total=2, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    return session

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")
    print(f"{Fore.GREEN}[OK] Ghost Tunnel: HIGH-SPEED ACTIVE")

def clean_and_verify(raw_html, target, report_file, source_label):
    try:
        soup = BeautifulSoup(raw_html, 'lxml')
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]): 
            script.decompose()
        text = soup.get_text(separator=' ')
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) < 10: continue
            noise_words = ["skip to content", "mobile english", "one last step", "javascript", "browser", "search about", "open links"]
            if any(noise in line.lower() for noise in noise_words): continue
            id_found = any(re.search(pattern, line) for pattern in SURE_HITS.values())
            if (target.lower() in line.lower()) or id_found:
                with print_lock:
                    display_text = " ".join(line.split())[:250]
                    print(f"{Fore.RED}[{source_label}-FOUND] {Fore.WHITE}{display_text}")
                    with open(report_file, "a") as f: f.write(f"[{source_label}] {line}\n")
    except: pass

def pdf_document_finder(target, report_file):
    # ADVANCED DORKS: Scanning HTTP and HTTPS results for documents and registrations
    dorks = [
        f"https://www.google.com/search?q=inurl:http OR inurl:https %22{target}%22 filetype:pdf OR filetype:xls",
        f"https://www.google.com/search?q=%22{target}%22 + \"login\" OR \"signup\" OR \"portal\"",
        f"https://www.bing.com/search?q=%22{target}%22 + site:*.in OR site:*.gov.in"
    ]
    for url in dorks:
        try:
            res = requests.get(url, timeout=12, headers=headers)
            # Find links from both http and https sources
            links = re.findall(r'(https?://[^\s<>"]+\.(?:pdf|doc|xls|xlsx|docx))', res.text)
            for link in links:
                with print_lock:
                    print(f"{Fore.YELLOW}[DOC-LINK] {Fore.WHITE}{link}")
            clean_and_verify(res.text, target, report_file, "WEB-DATA")
        except: pass

def telegram_dork_engine(target, report_file):
    tg_links = [
        f"https://www.google.com/search?q=site:t.me OR site:telegram.me %22{target}%22",
        f"https://yandex.com/search/?text=%22{target}%22 site:t.me"
    ]
    for url in tg_links:
        try:
            res = requests.get(url, timeout=12, headers=headers)
            clean_and_verify(res.text, target, report_file, "TG-DATA")
        except: pass

def shadow_crawler_ai(target, report_file):
    # Scanning both Clearnet (HTTP/HTTPS) and Darknet (Onion)
    gateways = [
        f"https://ahmia.fi/search/?q={target}+leak",
        f"https://psbdmp.ws/api/search/{target}",
        f"https://www.google.com/search?q=site:pastebin.com OR site:ghostbin.co OR site:controlc.com %22{target}%22"
    ]
    session = get_onion_session()
    for url in gateways:
        try:
            is_onion = "ahmia" in url
            res = (session if is_onion else requests).get(url, timeout=15, headers=headers)
            clean_and_verify(res.text, target, report_file, "LEAK-DATA")
        except: pass

def silent_tool_runner(cmd, name, report_file):
    try:
        process = subprocess.Popen(f"torsocks {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            clean = line.strip()
            if any(x in clean.lower() for x in ["http", "found", "match:"]):
                with print_lock:
                    print(f"{Fore.GREEN}[{name.upper()}-HIT] {Fore.WHITE}{clean}")
                    with open(report_file, "a") as f: f.write(f"[{name}] {clean}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║        KHALID HUSAIN INVESTIGATOR - FULL SCAN v75.0          ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/PAN/ID): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")
    if os.path.exists(report_path): os.remove(report_path)
    
    print(f"{Fore.BLUE}[*] Advanced Discovery: Scanning HTTP, HTTPS, Social & Dark Web...\n")
    threads = [
        Thread(target=pdf_document_finder, args=(target, report_path)),
        Thread(target=telegram_dork_engine, args=(target, report_path)),
        Thread(target=shadow_crawler_ai, args=(target, report_path)),
        Thread(target=silent_tool_runner, args=(f"sherlock {target} --timeout 10", "Sherlock", report_path)),
        Thread(target=silent_tool_runner, args=(f"maigret {target} --timeout 10", "Maigret", report_path))
    ]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"\n{Fore.GREEN}[➔] Investigation Complete. Detailed Report Saved: {report_path}")

if __name__ == "__main__":
    main()
