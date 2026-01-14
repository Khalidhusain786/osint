```python
import os, subprocess, sys, requests, re, time, random
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import markdown
from weasyprint import HTML
import json
import urllib.parse

init(autoreset=True)
print_lock = Lock()

# --- NEW: ANISH EXPLOITS & TELEGRAM BOTS ---
ANISH_EXPLOIT_URL = "https://anishexploits.site/app/"
ANISH_PASSWORD = "Anish123"
TELEGRAM_BOTS = [
    "@number_infobot", "@osinttghighbot", "@TrueOsintBot", 
    "@Hiddnosint_bot", "@breached_data_breacheddatabot"
]

# --- COMPREHENSIVE DATA PATTERNS (EXPANDED) ---
SURE_HITS = {
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "Aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b|\b\d{12}\b",
    "Passport": r"[A-Z][0-9]{7}|[A-Z]{2}\d{7}",
    "Bank_Acc": r"\b[0-9]{9,18}\b",
    "VoterID": r"[A-Z]{3}[0-9]{7}",
    "Phone": r"(?:\+91|0)?[6-9]\d{9}",
    "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "Pincode": r"\b\d{6}\b",
    "Vehicle": r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}",
    "IP": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "BTC": r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b",
    "ETH": r"0x[a-fA-F0-9]{40}",
    "Password": r"(?i)(password|pass|pwd|key):?\s*([^\s\"\'<>]{4,50})",
    "Address": r"(?i)([A-Z]{1,2}/?\d+|[HSF]No\.?\s?\d+|[P]lot\s?\d+)(?:\s+(?:Street|Road|Lane|Gal?i|Block|Mohalla|Colony|Sector|Area| Nagar| Vihar))?",
    "Photo": r"(?i)(jpg|jpeg|png|gif|webp|photo|image|avatar|profile_pic)",
    "Document": r"(?i)(pdf|docx|doc|xlsx|csv|txt|xml|json|zip|rar)"
}

def get_headers():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ]
    return {"User-Agent": random.choice(agents)}

def get_tor_session():
    session = requests.Session()
    try:
        proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        session.proxies.update(proxies)
    except: pass
    return session

# --- ANISH EXPLOITS ACCESS ---
def anish_exploits_scan(phone_number, findings):
    try:
        print(f"{Fore.MAGENTA}[🔓] ANISH EXPLOITS - Auto-login active...")
        
        # Step 1: Access main page
        session = requests.Session()
        session.headers.update(get_headers())
        res = session.get(ANISH_EXPLOIT_URL, timeout=15)
        
        # Step 2: Auto-submit password
        payload = {
            'password': ANISH_PASSWORD,
            'submit': 'Login'
        }
        res = session.post(ANISH_EXPLOIT_URL, data=payload, timeout=15)
        
        # Step 3: Submit phone number
        phone_payload = {
            'phone': phone_number,
            'search': 'Search'
        }
        res = session.post(ANISH_EXPLOIT_URL, data=phone_payload, timeout=15)
        
        # Extract all data
        hits = extract_hits(res.text, phone_number, "ANISH_EXPLOITS")
        if hits:
            with print_lock:
                print(f"{Fore.RED}🔥 ANISH EXPLOITS HIT! {Fore.WHITE}{len(hits)} records")
                for hit in hits:
                    print(f"  {Fore.CYAN}→ {hit}")
            
            findings["ANISH_EXPLOITS"] = hits
            
    except Exception as e:
        print(f"{Fore.YELLOW}[ANISH] Connection issue: {e}")

# --- TELEGRAM BOTS ---
def telegram_bot_scan(target, findings):
    print(f"{Fore.BLUE}[🤖] TELEGRAM BOTS ACTIVE...")
    bot_urls = [
        
        f"https://www.google.com/search?q={urllib.parse.quote(target)}+site:t.me/{bot[1:]}"
        for bot in TELEGRAM_BOTS
    ]
    
    for bot_url in bot_urls:
        scan_engine(bot_url, target, findings, "TG_BOT", use_tor=False)

# --- DARK/WEB DEEP WEB ENGINES ---
DARK_DEEP_ENGINES = [
    "https://ahmia.fi/search/?q={}",
    "https://dark.fail/search?q={}",
    "https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/?q={}",
    "http://search7tdrcvri22rieiwgi5g46qnwsesvnubqav2xakhezv4hjzkkad.onion/search/?q={}",
    "https://intelx.io/search?q={}&media=website"
]

# --- SOCIAL MEDIA PLATFORMS ---
SOCIAL_PLATFORMS = [
    "https://www.facebook.com/search/top?q={}",
    "https://twitter.com/search?q={}&src=typed_query",
    "https://www.instagram.com/explore/search/keyword/?q={}",
    "https://www.linkedin.com/search/results/all/?keywords={}",
    "https://www.reddit.com/search/?q={}",
    "https://t.me/search?query={}",
    "https://www.quora.com/search?q={}"
]

# --- GOVERNMENT & DOC ENGINES (ALL DOC TYPES) ---
GOV_DOC_SITES = [
    "https://www.google.com/search?q={}+site:gov.in+OR+site:nic.in",
    "https://www.google.com/search?q={}+filetype:pdf+OR+filetype:doc+OR+filetype:docx+OR+filetype:xlsx",
    "https://www.india.gov.in/search/node/{}",
    "https://www.google.com/search?q={}+site:nic.in+OR+site:gov.in+intitle:\"index of\"",
    "https://www.google.com/search?q={}+\"pan card\"+OR+\"aadhaar\"+OR+\"passport\"+filetype:pdf"
]

# --- COMPANY & LEAK SITES ---
COMPANY_LEAKS = [
    "https://www.google.com/search?q={}+site:pastebin.com+OR+site:github.com",
    "https://psbdmp.ws/search/{}",
    "https://controlc.com/search?q={}",
    "https://leak-lookup.com/search?q={}"
]

def extract_hits(html_content, target, source):
    hits = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 5]
        
        for line in lines:
            # Target match
            if target.lower() in line.lower() and len(line) < 300:
                hits.append(line)
            
            # Pattern matches (ALL passwords shown)
            for pattern_name, pattern in SURE_HITS.items():
                matches = re.findall(pattern, line)
                if matches:
                    if pattern_name == "Password":
                        # Show ALL passwords found
                        for pwd in matches[1] if isinstance(matches[1], list) else [matches[1]]:
                            if len(pwd) > 3 and len(pwd) < 100:
                                hits.append(f"[{pattern_name}] {pwd}")
                    else:
                        hits.append(f"[{pattern_name}] {line[:250]}")
                    break
                    
        # Extract ALL links (documents, photos, etc.)
        links = re.findall(r'https?://[^\s<>"]+', html_content)
        for link in links:
            if any(ext in link.lower() for ext in ['pdf','doc','jpg','png','zip','rar']) or target in link:
                hits.append(f"[LINK] {link}")
                
    except: pass
    return hits

def scan_engine(url_template, target, findings, source_label, use_tor=False):
    try:
        session = get_tor_session() if use_tor else requests.Session()
        url = url_template.format(urllib.parse.quote(target).replace('%20','+'))
        res = session.get(url, headers=get_headers(), timeout=12)
        
        hits = extract_hits(res.text, target, source_label)
        if hits:
            with print_lock:
                print(f"{Fore.CYAN}[{source_label}] {Fore.RED}✓{Fore.WHITE} {len(hits)} hits")
                for hit in hits[:8]:  # Increased from 3 to 8
                    print(f"  {Fore.WHITE}{hit}")
            
            if source_label not in findings:
                findings[source_label] = []
            findings[source_label].extend(hits)
            
    except: pass

def intel_breach_scan(target, findings):
    intel_services = [
        ("INTELX", "https://intelx.io/search?q={}&termtype=all"),
        ("SCYLLA", "https://scylla.one/?q={target}"),
        ("GHOSTPROJ", "https://ghostproject.fr/?s={target}"),
        ("SNUSBASE", "https://snusbase.com/search?q={target}"),
        ("LEAKCHECK", "https://leakcheck.io/api/search?q={target}")
    ]
    
    for name, url in intel_services:
        scan_engine(url.format(target), target, findings, name)

def full_spectrum_scan(target, findings):
    """Run ALL scanners"""
    scanners = [
        (intel_breach_scan, (target, findings)),
        (lambda: darkweb_scan(target, findings)),
        (lambda: social_scan(target, findings)),
        (lambda: gov_doc_scan(target, findings)),
        (lambda: company_leak_scan(target, findings)),
        (lambda: telegram_bot_scan(target, findings))
    ]
    
    threads = []
    for func, args in scanners:
        t = Thread(target=func, args=args if len(args) > 1 else ())
        t.start()
        threads.append(t)
        time.sleep(0.2)
    
    for t in threads:
        t.join()

def darkweb_scan(target, findings):
    print(f"{Fore.BLUE}[🌑] Dark/Deep Web...")
    for engine in DARK_DEEP_ENGINES:
        scan_engine(engine.format(target), target, findings, "DARKWEB", use_tor=True)

def social_scan(target, findings):
    print(f"{Fore.BLUE}[📱] Social Media...")
    for platform in SOCIAL_PLATFORMS:
        scan_engine(platform.format(target), target, findings, "SOCIAL")

def gov_doc_scan(target, findings):
    print(f"{Fore.BLUE}[🏛️] Government Documents...")
    for gov_site in GOV_DOC_SITES:
        scan_engine(gov_site.format(target), target, findings, "GOV-DOCS")

def company_leak_scan(target, findings):
    print(f"{Fore.BLUE}[🏢] Company Leaks...")
    for leak_site in COMPANY_LEAKS:
        scan_engine(leak_site.format(target), target, findings, "COMPANY")

def generate_pdf_report(target, findings):
    if not findings:
        print(f"{Fore.YELLOW}[!] No data found for {target}")
        return
    
    markdown_content = f"# 🔥 ULTIMATE OSINT REPORT v80.1 🔥\n\n"
    markdown_content += f"**Target:** `{target}` | **Total Sources:** {len(findings)}\n"
    markdown_content += f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S UTC')} | **Total Records:** {sum(len(h) for h in findings.values())}\n\n"
    
    for source, hits in sorted(findings.items()):
        if hits:
            markdown_content += f"## {source}\n\n"
            for i, hit in enumerate(hits, 1):
                markdown_content += f"{i}. **{hit}**\n"
            markdown_content += "\n```\n```\n\n"
    
    pdf_file = f"{target.replace(' ', '_')}.pdf"
    try:
        HTML(string=markdown_content).write_pdf(pdf_file)
        print(f"\n{Fore.GREEN}[📄] {Fore.WHITE}{pdf_file} {Fore.GREEN}GENERATED!")
        print(f"{Fore.CYAN}📊 {sum(len(h) for h in findings.values())} total records across {len(findings)} sources")
        os.system(f"open '{pdf_file}' 2>/dev/null || xdg-open '{pdf_file}' 2>/dev/null")
    except:
        md_file = f"{target.replace(' ', '_')}.md"
        with open(md_file, 'w') as f:
            f.write(markdown_content)
        print(f"{Fore.YELLOW}[📝] {md_file} saved!")

def main():
    os.system('clear')
    print(f"{Fore.RED}🚀 KHALID HUSAIN v80.1 - ANISH+TG_BOTS+ALL_DOCS+FULL_LEAKS 🚀")
    print("=" * 90)
    
    target = input(f"{Fore.WHITE}🎯 Target (Phone/Name/Email/PAN): ").strip()
    if not target:
        return

    print(f"\n{Fore.GREEN}[⚡] FULL SPECTRUM + ANISH EXPLOITS + TG BOTS ACTIVE...")
    findings = {}
    
    # ANISH EXPLOITS (Phone only for this service)
    if re.match(r"(?:\+91|0)?[6-9]\d{9}", target):
        anish_thread = Thread(target=anish_exploits_scan, args=(target, findings))
        anish_thread.start()
    
    # Full spectrum scan
    full_thread = Thread(target=full_spectrum_scan, args=(target, findings))
    full_thread.start()
    
    # Wait for completion
    if 'anish_thread' in locals():
        anish_thread.join()
    full_thread.join()
    
    generate_pdf_report(target, findings)

if __name__ == "__main__":
    main()
```

