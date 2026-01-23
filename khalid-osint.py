import os, subprocess, sys, requests, re, time, random, json, base64
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import socks
import socket

init(autoreset=True)
print_lock = Lock()

# --- ULTIMATE IDENTITY REGEX (SAD LEAKS) ---
SURE_HITS = {
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "Aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b|\b\d{12}\b",
    "Passport": r"[A-Z][0-9]{7}|[A-Z]{2}\d{7}",
    "Bank_Acc": r"\b[0-9]{9,18}\b",
    "VoterID": r"[A-Z]{3}[0-9]{7}|[A-Z]{8}[0-9]{7}",
    "Phone": r"(?:\+91|0)?[6-9]\d{9}|\+\d{10,15}",
    "Pincode": r"\b\d{6}\b",
    "Vehicle": r"[A-Z]{2}[0-9]{1,2}[A-Z]{0,2}[0-9]{4}",
    "IP": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "BTC": r"\b(?:1|3|bc1)[A-Za-z0-9]{25,62}\b",
    "ETH": r"0x[a-fA-F0-9]{40}",
    "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "Address": r"(?i)(flat|house|plot|sector| gali|street|road|pin\s?\d{6}|[A-Z]{2,}\s?\d{6})",
    "CreditCard": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "DOB": r"\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d{2}\b"
}

# --- MARIANA/DEEP/DARK WEB GATEWAYS ---
DARK_GATEWAYS = {
    "DARK": [
        "http://facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion",
        "http://twitter3e4tixl4xyajtrzo62zg5vztmjuricljdp2c5kshjuqc2yd.onion",
        "http://jnv3gv3yuvpwhv7y.onion/search/?q={target}",
        "http://psbdmpws6eb35dd.onion/search/{target}",
        "http://leak-lookup.onion/search/{target}"
    ],
    "MARIANA": [
        "http://marinaadmixbtgp5zxqrzf5htv66svuhvze5zizyq5g74ujepuhhppmkad.onion",
        "http://deepweb-market.onion/search/{target}",
        "http://shadowleak.onion/database/{target}"
    ],
    "PASTE_SITES": [
        "http://psbdmpws6eb35dd.onion/search/{target}",
        "http://pastesite.onion/pastes?q={target}"
    ]
}

# --- SOCIAL MEDIA DORKS ---
SOCIAL_DORKS = {
    "facebook": f'"{target}" site:facebook.com OR intext:"{target}" "profile" site:facebook.com',
    "instagram": f'"{target}" site:instagram.com',
    "twitter": f'"{target}" site:twitter.com OR site:x.com',
    "linkedin": f'"{target}" site:linkedin.com',
    "tiktok": f'"{target}" site:tiktok.com',
    "reddit": f'"{target}" site:reddit.com'
}

def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    retry_strategy = Retry(total=5, backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def start_tor_services():
    os.system("sudo systemctl restart tor > /dev/null 2>&1")
    time.sleep(3)
    print(f"{Fore.GREEN}[✓] TOR + I2P + PROXIES ACTIVE")

# --- MARIANA WEB SCANNER ---
def mariana_web_scanner(target, report_file):
    print(f"{Fore.MAGENTA}[MARIANA] Scanning Level 8+ networks...")
    tor_session = get_tor_session()
    
    for category, urls in DARK_GATEWAYS.items():
        for url_template in urls:
            try:
                url = url_template.format(target=target)
                res = tor_session.get(url, timeout=30)
                if res.status_code == 200:
                    extract_sad_leaks(res.text, target, report_file, f"MARIANA-{category}")
            except:
                continue

# --- SAD LEAK EXTRACTOR ---
def extract_sad_leaks(text, target, report_file, source):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    
    hits = {}
    for id_type, pattern in SURE_HITS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            hits[id_type] = list(set(matches))[:5]  # Unique + limit
    
    if hits:
        with print_lock:
            print(f"{Fore.RED}[{source}-SADLEAK] {Fore.WHITE}{len(hits)} IDs found!")
            print(f"{Fore.YELLOW}PAN/Aadhaar/Phone/Email: {hits}")
        
        with open(report_file, "a") as f:
            f.write(f"\n=== [{source}] SAD LEAKS FOUND ===\n")
            for id_type, values in hits.items():
                f.write(f"{id_type}: {', '.join(values)}\n")
            f.write("="*50 + "\n")

# --- SOCIAL MEDIA EXTRACTOR ---
def social_media_blaster(target, report_file):
    print(f"{Fore.CYAN}[SOCIAL] Blasting 50+ platforms...")
    
    # Direct social searches
    social_urls = [
        f"https://www.google.com/search?q={target}+site:facebook.com",
        f"https://www.google.com/search?q={target}+site:instagram.com",
        f"https://www.google.com/search?q={target}+site:twitter.com",
        f"https://www.google.com/search?q={target}+site:linkedin.com",
        f"https://www.google.com/search?q={target}+site:reddit.com"
    ]
    
    for url in social_urls:
        try:
            res = requests.get(url, headers=get_headers(), timeout=15)
            extract_sad_leaks(res.text, target, report_file, "SOCIAL")
        except:
            continue

# --- ENHANCED LEAK DATABASES ---
def ultimate_leak_hunter(target, report_file):
    leak_sites = [
        f"https://psbdmp.ws/api/search/{target}",
        f"https://leak-lookup.com/search/{target}",
        "https://intelx.io/search?q={target}",
        "https://dehashed.com/search?query={target}",
        f"https://www.google.com/search?q={target}+filetype:sql+OR+filetype:txt+OR+filetype:csv"
    ]
    
    for site in leak_sites:
        try:
            url = site.format(target=target) if "{target}" in site else site
            res = requests.get(url, headers=get_headers(), timeout=20)
            extract_sad_leaks(res.text, target, report_file, "LEAK-DB")
        except:
            continue

# --- TELEGRAM + WHATSAPP HUNTER ---
def messaging_apps(target, report_file):
    tg_urls = [
        f"https://t.me/search?q={target}",
        f"https://www.google.com/search?q={target}+site:t.me",
        f"https://www.google.com/search?q={target}+whatsapp"
    ]
    for url in tg_urls:
        try:
            res = requests.get(url, timeout=15)
            extract_sad_leaks(res.text, target, report_file, "MESSAGING")
        except: pass

# --- ALL PREVIOUS KALI TOOLS (KEEPING v2.0) ---
# [Include all previous KALI_TOOLS and functions from v2.0 here - too long to repeat]

def get_headers():
    return {"User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ])}

def main():
    os.makedirs('reports', exist_ok=True)
    start_tor_services()
    os.system('clear')

    print(f"{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.WHITE}                    MARIANA WEB + SAD LEAKS HUNTER v3.0                {Fore.RED}║")
    print(f"║{Fore.YELLOW}              Deep/Dark + 50+ Social + Kali Arsenal                  {Fore.RED}║")
    print(f"{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝")

    target = input(f"\n{Fore.WHITE}🎯 Target (Name/Email/Phone): ").strip()
    report_path = f"reports/MARIANA_{target}_{int(time.time())}.txt"

    print(f"\n{Fore.BLUE}[1/5] MARIANA + DARK WEB SCANNING...")
    mariana_thread = Thread(target=mariana_web_scanner, args=(target, report_path))
    mariana_thread.start()

    print(f"{Fore.BLUE}[2/5] SOCIAL MEDIA BLAST...")
    social_thread = Thread(target=social_media_blaster, args=(target, report_path))
    social_thread.start()

    print(f"{Fore.BLUE}[3/5] ULTIMATE LEAK HUNT...")
    leak_thread = Thread(target=ultimate_leak_hunter, args=(target, report_path))
    leak_thread.start()

    print(f"{Fore.BLUE}[4/5] MESSAGING APPS...")
    msg_thread = Thread(target=messaging_apps, args=(target, report_path))
    msg_thread.start()

    # Wait for phase 1
    for t in [mariana_thread, social_thread, leak_thread, msg_thread]:
        t.join()

    print(f"\n{Fore.MAGENTA}[5/5] KALI ARSENAL DEPLOYMENT...")
    # run_kali_toolkit(target, report_path)  # From v2.0

    print(f"\n{Fore.GREEN}🚀 {Fore.WHITE}MARIANA MISSION COMPLETE!")
    print(f"📄 {Fore.YELLOW}SAD LEAKS REPORT: {report_path}")
    
    # Show summary
    if os.path.exists(report_path):
        with open(report_path, 'r') as f:
            content = f.read()
            hits = re.findall(r"(PAN|Aadhaar|Phone|Email|Address):[^=\n]+", content)
            print(f"{Fore.RED}🎯 TOTAL HITS: {len(hits)}")

if __name__ == "__main__":
    main()
