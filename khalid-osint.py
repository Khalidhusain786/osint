import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

init(autoreset=True)
print_lock = Lock()

# --- EXTENDED TARGET IDENTITY FILTERS ---
SURE_HITS = {
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "Aadhaar": r"\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b",
    "Passport": r"[A-Z][0-9]{7}",
    "Bank_Acc": r"\b[0-9]{9,18}\b",
    "VoterID": r"[A-Z]{3}[0-9]{7}",
    "Phone": r"(?:\+91|0)?[6-9]\d{9}",
    "Pincode": r"\b\d{6}\b",
    "Vehicle": r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}",
    "IP_Address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "BTC_Address": r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b",
    "Address": r"(?i)(Gali\s?No|H\.No|Plot|Sector|Ward|Tehsil|District|PIN:)",
    "Relations": r"(?i)(Father|Mother|W/O|S/O|D/O|Relative|Alternative|Nominee)",
    "Location": r"(?i)(Village|City|State|Country|Map|Lat|Long)"
}

def get_onion_session():
    session = requests.Session()
    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    session.proxies.update(proxies)
    retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    return session

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")
    print(f"{Fore.GREEN}[OK] Ghost Tunnel: HTTP/HTTPS/ONION PROTOCOLS ACTIVE")

def clean_and_verify(raw_html, target, report_file, source_label):
    try:
        soup = BeautifulSoup(raw_html, 'lxml')
        for junk in soup(["script", "style", "nav", "header", "footer", "aside"]): 
            junk.decompose()
        text = soup.get_text(separator=' ')
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) < 15: continue
            if any(x in line.lower() for x in ["search about", "open links", "javascript"]): continue
            
            id_found = any(re.search(pattern, line) for pattern in SURE_HITS.values())
            if (target.lower() in line.lower()) or id_found:
                clean_line = " ".join(line.split())[:300]
                with print_lock:
                    print(f"{Fore.RED}[{source_label}-HIT] {Fore.WHITE}{clean_line}")
                    with open(report_file, "a") as f: f.write(f"[{source_label}] {clean_line}\n")
    except: pass

# --- NEW: DATA BREACH CHECKER (HIBP API) ---
def check_breach_databases(target, report_file):
    if "@" in target:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}"
        # Note: Needs API Key for full use, but standard dorks can also find leak mentions
        try:
            res = requests.get(f"https://www.google.com/search?q=%22{target}%22+site:leak-lookup.com+OR+site:intelx.io", headers=headers)
            clean_and_verify(res.text, target, report_file, "BREACH-INFO")
        except: pass

def http_protocol_finder(target, report_file):
    dorks = [
        f"https://www.google.com/search?q=inurl:http:// -inurl:https:// %22{target}%22",
        f"https://www.bing.com/search?q=%22{target}%22 + \"index of\" + http",
        f"https://yandex.com/search/?text=site:*.in %22{target}%22"
    ]
    for url in dorks:
        try:
            res = requests.get(url, timeout=15, headers=headers)
            links = re.findall(r'(https?://[^\s<>"]+|[a-z2-7]{56}\.onion)', res.text)
            for link in links:
                if target in link:
                    with print_lock: print(f"{Fore.YELLOW}[LINK-FOUND] {Fore.WHITE}{link}")
            clean_and_verify(res.text, target, report_file, "HTTP-WEB")
        except: pass

def advanced_onion_scanner(target, report_file):
    onion_gateways = [
        f"http://jnv3gv3yuvpwhv7y.onion/search/?q={target}", 
        f"https://ahmia.fi/search/?q={target}",               
        f"http://phishsetvsnm4v5n.onion/search.php?q={target}" 
    ]
    session = get_onion_session()
    for url in onion_gateways:
        try:
            res = session.get(url, timeout=25, headers=headers)
            clean_and_verify(res.text, target, report_file, "DARK-DEEP")
        except: pass

def telegram_dork_engine(target, report_file):
    tg_links = [
        f"https://www.google.com/search?q=site:t.me OR site:telegram.me %22{target}%22",
        f"https://yandex.com/search/?text=%22{target}%22 site:t.me"
    ]
    for url in tg_links:
        try:
            res = requests.get(url, timeout=15, headers=headers)
            clean_and_verify(res.text, target, report_file, "TG-DATA")
        except: pass

def shadow_crawler_ai(target, report_file):
    gateways = [
        f"https://psbdmp.ws/api/search/{target}",
        f"https://www.google.com/search?q=site:pastebin.com OR site:ghostbin.co OR site:controlc.com %22{target}%22"
    ]
    for url in gateways:
        try:
            res = requests.get(url, timeout=15, headers=headers)
            clean_and_verify(res.text, target, report_file, "LEAK-DB")
        except: pass

def silent_tool_runner(cmd, name, report_file):
    try:
        process = subprocess.Popen(f"torsocks {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            clean = line.strip()
            if any(x in clean.lower() for x in ["http", "found", "match:", "onion"]):
                with print_lock:
                    print(f"{Fore.GREEN}[{name.upper()}-HIT] {Fore.WHITE}{clean}")
                    with open(report_file, "a") as f: f.write(f"[{name}] {clean}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    banner() {
    clear
    printf "\e[1;92m"
    printf "  ██╗  ██╗██╗  ██╗ █████╗ ██╗     ██╗██████╗ \n"
    printf "  ██║ ██╔╝██║  ██║██╔══██╗██║     ██║██╔══██╗\n"
    printf "  █████╔╝ ███████║███████║██║     ██║██║  ██║\n"
    printf "  ██╔═██╗ ██╔══██║██╔══██║██║     ██║██║  ██║\n"
    printf "  ██║  ██╗██║  ██║██║  ██║███████╗██║██████╔╝\n"
    printf "  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ \n"
    printf "       \e[1;93mH  U  S  A  I  N    7  8  6\e[0m\n"
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/PAN/ID): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")
    if os.path.exists(report_path): os.remove(report_path)
    
    print(f"{Fore.BLUE}[*] Full-Spectrum Scan: Breach DBs, HTTP, Onion, Deep & Dark Web...\n")
    threads = [
        Thread(target=http_protocol_finder, args=(target, report_path)),
        Thread(target=advanced_onion_scanner, args=(target, report_path)),
        Thread(target=telegram_dork_engine, args=(target, report_path)),
        Thread(target=shadow_crawler_ai, args=(target, report_path)),
        Thread(target=check_breach_databases, args=(target, report_path)),
        Thread(target=silent_tool_runner, args=(f"sherlock {target} --timeout 10", "Sherlock", report_path)),
        Thread(target=silent_tool_runner, args=(f"maigret {target} --timeout 10", "Maigret", report_path))
    ]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"\n{Fore.GREEN}[➔] Investigation Complete. Comprehensive Report: {report_path}")

if __name__ == "__main__":
    main()
