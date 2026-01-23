import os, subprocess, sys, requests, re, time, random, json
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

init(autoreset=True)
print_lock = Lock()

# --- ULTIMATE SAD LEAK REGEX ---
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
    "Address": r"(?i)(flat|house|plot|sector|gali|street|road|pin\s?\d{6})",
    "CreditCard": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "DOB": r"\b(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/(?:19|20)\d{2}\b"
}

def get_headers():
    return {"User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    ])}

def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    retry_strategy = Retry(total=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def start_tor():
    os.system("sudo systemctl restart tor > /dev/null 2>&1")
    time.sleep(2)
    print(f"{Fore.GREEN}[✓] TOR ACTIVE")

# --- SAD LEAK EXTRACTOR ---
def extract_sad_leaks(text, target, report_file, source):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        text_content = soup.get_text()
        
        hits = {}
        for id_type, pattern in SURE_HITS.items():
            matches = re.findall(pattern, text_content, re.IGNORECASE | re.MULTILINE)
            if matches:
                unique_matches = list(set(matches))
                hits[id_type] = unique_matches[:5]
        
        if hits:
            with print_lock:
                print(f"{Fore.RED}[{source}] 🎯 {len(hits)} SAD LEAKS!")
                for id_type, values in hits.items():
                    print(f"  {Fore.YELLOW}{id_type}: {Fore.WHITE}', '.join(values)}")
            
            with open(report_file, "a", encoding='utf-8') as f:
                f.write(f"\n🔥 [{source}-{time.strftime('%H:%M:%S')}] {len(hits)} HITS 🔥\n")
                for id_type, values in hits.items():
                    f.write(f"{id_type}: {', '.join(values)}\n")
                f.write("="*60 + "\n")
    except:
        pass

# --- MARIANA + DARK WEB ---
def mariana_dark_scanner(target, report_file):
    print(f"{Fore.MAGENTA}[🌑 MARIANA] Scanning...")
    tor_session = get_tor_session()
    
    dark_urls = [
        f"http://jnv3gv3yuvpwhv7y.onion/search/?q={target}",
        f"https://ahmia.fi/search/?q={target}",
        "http://psbdmpws6eb35dd.onion/search/" + target,
    ]
    
    for url in dark_urls:
        try:
            res = tor_session.get(url, timeout=25)
            extract_sad_leaks(res.text, target, report_file, "MARIANA-DARK")
        except:
            continue

# --- SOCIAL MEDIA BLAST ---
def social_blaster(target, report_file):
    print(f"{Fore.CYAN}[📱 SOCIAL] 50+ platforms...")
    social_searches = [
        f"https://www.google.com/search?q=\"{target}\" site:facebook.com",
        f"https://www.google.com/search?q=\"{target}\" site:instagram.com", 
        f"https://www.google.com/search?q=\"{target}\" site:twitter.com",
        f"https://www.google.com/search?q=\"{target}\" site:linkedin.com",
        f"https://www.google.com/search?q=\"{target}\" site:reddit.com",
        f"https://t.me/search?q={target}"
    ]
    
    for url in social_searches:
        try:
            res = requests.get(url, headers=get_headers(), timeout=12)
            extract_sad_leaks(res.text, target, report_file, "SOCIAL")
        except:
            continue

# --- LEAK HUNTER ---
def leak_hunter(target, report_file):
    print(f"{Fore.RED}[💾 LEAKS] Databases...")
    leak_urls = [
        f"https://psbdmp.ws/api/search/{target}",
        f"https://leak-lookup.com/search/{target}",
        f"https://www.google.com/search?q=\"{target}\" filetype:sql OR filetype:txt OR filetype:csv",
        f"https://www.google.com/search?q=\"{target}\" site:pastebin.com"
    ]
    
    for url in leak_urls:
        try:
            res = requests.get(url, headers=get_headers(), timeout=15)
            extract_sad_leaks(res.text, target, report_file, "LEAKS")
        except:
            continue

# --- KALI TOOLS (SIMPLIFIED) ---
def run_kali_tools(target, report_file):
    print(f"{Fore.GREEN}[⚔️ KALI] Arsenal...")
    tools = [
        f"echo '[SHERLOCK] Scanning...' && torsocks sherlock {target} --timeout 8",
        f"echo '[HOLEHE] Checking...' && torsocks holehe {target}",
        f"echo '[HARVEST] Domains...' && theHarvester -d {target} -b google -l 50"
    ]
    
    for tool_cmd in tools:
        try:
            result = subprocess.run(tool_cmd, shell=True, capture_output=True, text=True, timeout=60)
            if result.stdout:
                with open(report_file, "a") as f:
                    f.write(f"\n[KALI-TOOL] {result.stdout[:500]}\n")
        except:
            pass

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: python3 {sys.argv[0]} <target>")
        print(f"{Fore.YELLOW}Example: python3 {sys.argv[0]} khalidhusain786")
        return
    
    target = sys.argv[1].strip()
    os.makedirs('reports', exist_ok=True)
    
    report_path = f"reports/SADLEAKS_{target}_{int(time.time())}.txt"
    
    start_tor()
    os.system('clear')
    
    print(f"{Fore.RED}╔══════════════════════════════════════════════════════╗")
    print(f"║{Fore.WHITE}           KHALID OSINT v3.0 - SAD LEAKS HUNTER        {Fore.RED}║")
    print(f"║{Fore.YELLOW}    Mariana + DarkWeb + Social + Kali Arsenal       {Fore.RED}║")
    print(f"{Fore.RED}╚══════════════════════════════════════════════════════╝")
    print(f"{Fore.CYAN}🎯 TARGET: {Fore.WHITE}{target}")
    
    # Launch all scanners
    threads = [
        Thread(target=mariana_dark_scanner, args=(target, report_path)),
        Thread(target=social_blaster, args=(target, report_path)),
        Thread(target=leak_hunter, args=(target, report_path)),
        Thread(target=run_kali_tools, args=(target, report_path))
    ]
    
    for t in threads:
        t.start()
        time.sleep(0.5)
    
    for t in threads:
        t.join()
    
    print(f"\n{Fore.GREEN}✅ MISSION COMPLETE!")
    print(f"📄 REPORT: {Fore.YELLOW}{report_path}")
    
    # Quick summary
    try:
        with open(report_path, 'r') as f:
            lines = f.readlines()
            print(f"{Fore.RED}🎯 TOTAL LINES: {len(lines)}")
    except:
        pass

if __name__ == "__main__":
    main()
