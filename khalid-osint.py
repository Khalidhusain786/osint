import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

init(autoreset=True)
print_lock = Lock()

# --- TARGET IDENTITY FILTERS ---
SURE_HITS = {
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "Passport": r"[A-Z][0-9]{7}",
    "Bank_Acc": r"\b[0-9]{9,18}\b",
    "VoterID": r"[A-Z]{3}[0-9]{7}",
    "Phone": r"(?:\+91|0)?[6-9]\d{9}",
    "Pincode": r"\b\d{6}\b",
    "Address": r"(?i)(Gali\s?No|House\s?No|H\.No|Plot\s?No|Floor|Sector|Ward|Tehsil|District|Resident|PIN:)"
}

def get_onion_session():
    session = requests.Session()
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    session.proxies.update(proxies)
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")
    try:
        test_session = get_onion_session()
        test_session.get("http://check.torproject.org", timeout=10)
        print(f"{Fore.GREEN}[OK] Ghost Tunnel: HIGH-SPEED ACTIVE")
    except:
        print(f"{Fore.RED}[!] Tor is running but connection is weak.")

def clean_and_verify(raw_html, target, report_file, source_label):
    """FIXED: More accurate detection to show hidden data"""
    try:
        soup = BeautifulSoup(raw_html, 'lxml')
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]): 
            script.decompose()
            
        text = soup.get_text(separator=' ')
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if len(line) < 5: continue
            
            # Smart Filtering: Target ya koi ID pattern milne par show karega
            id_found = False
            found_labels = []
            for label, pattern in SURE_HITS.items():
                if re.search(pattern, line):
                    id_found = True
                    found_labels.append(label)

            # Agar target ka naam ya koi ID match ho, toh result show karein
            if (target.lower() in line.lower()) or id_found:
                # Sirf Google ke technical kachre ko skip karein, real data ko nahi
                if any(x in line.lower() for x in ["one last step", "javascript is disabled"]):
                    continue

                with print_lock:
                    # Clean output display
                    display_text = line[:180].replace('\t', ' ').strip()
                    print(f"{Fore.RED}[{source_label}-FOUND] {Fore.WHITE}{display_text}")
                    if found_labels:
                        print(f"   {Fore.YELLOW}➔ Detected: {', '.join(found_labels)}")
                    
                    with open(report_file, "a") as f: 
                        f.write(f"[{source_label}] {line}\n")
    except: pass

def pdf_document_finder(target, report_file):
    dorks = [
        f"https://www.google.com/search?q=site:*.in OR site:*.com filetype:pdf %22{target}%22",
        f"https://www.google.com/search?q=%22{target}%22 + passport OR address filetype:pdf",
        f"https://www.bing.com/search?q=%22{target}%22 + filetype:doc OR filetype:docx"
    ]
    for url in dorks:
        try:
            res = requests.get(url, timeout=15, headers=headers)
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
        f"https://yandex.com/search/?text=site:t.me+%22{target}%22"
    ]
    for url in tg_links:
        try:
            res = requests.get(url, timeout=15, headers=headers)
            clean_and_verify(res.text, target, report_file, "TG-DATA")
        except: pass

def shadow_crawler_ai(target, report_file):
    gateways = [
        f"https://ahmia.fi/search/?q={target}+india+leak",
        f"https://psbdmp.ws/api/search/{target}",
        f"https://www.google.com/search?q=site:facebook.com+OR+site:instagram.com+%22{target}%22"
    ]
    session = get_onion_session()
    for url in gateways:
        try:
            res = session.get(url, timeout=20, headers=headers)
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
    print(f"{Fore.RED}║        KHALID HUSAIN INVESTIGATOR - ACCURATE MODE v74.0      ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/PAN): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")
    if os.path.exists(report_path): os.remove(report_path)
    print(f"{Fore.BLUE}[*] Searching Hidden Records with Onion Proxy...\n")
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
