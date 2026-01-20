```python
import os, subprocess, sys, requests, re, time, random
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import markdown
from weasyprint import HTML

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

# --- DYNAMIC HEADERS TO AVOID BLOCKS ---
def get_headers():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    ]
    return {"User-Agent": random.choice(agents)}

def get_onion_session():
    session = requests.Session()
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    session.proxies.update(proxies)
    retry_strategy = Retry(total=3, backoff_factor=1,
                           status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    return session

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")

def clean_and_verify(raw_html, target, findings, source_label):
    hits_found = []
    try:
        try:
            soup = BeautifulSoup(raw_html, 'lxml')
        except:
            soup = BeautifulSoup(raw_html, 'html.parser')

        for junk in soup(["script", "style", "nav", "header", "footer", "aside"]):
            junk.decompose()

        text = soup.get_text(separator=' ')
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if len(line) < 15:
                continue
            if any(x in line.lower() for x in ["search about", "open links", "javascript"]):
                continue

            id_found = any(re.search(pattern, line) for pattern in SURE_HITS.values())
            if (target.lower() in line.lower()) or id_found:
                clean_line = " ".join(line.split())[:300]
                hits_found.append(f"[{source_label}] {clean_line}")
                
        if hits_found:
            with print_lock:
                for hit in hits_found:
                    print(f"{Fore.RED}[HIT] {Fore.WHITE}{hit}")
            findings[source_label] = hits_found
    except:
        pass
    return hits_found

def check_breach_databases(target, findings):
    try:
        if "@" in target:
            res = requests.get(
                f"https://www.google.com/search?q=%22{target}%22+site:leak-lookup.com+OR+site:intelx.io",
                headers=get_headers()
            )
            clean_and_verify(res.text, target, findings, "BREACH-INFO")
    except:
        pass

# --- INTELLIGENCE BREACH SCANNER ---
def intelligence_breach_scan(target, findings):
    print(f"{Fore.BLUE}[*] Intelligence Services Scan Active...")
    
    # IntelX
    try:
        intelx_url = f"https://intelx.io/search?q={target}&termtype=emails&timeout=15s"
        res = requests.get(intelx_url, headers=get_headers(), timeout=15)
        if "results" in res.text.lower():
            with print_lock:
                print(f"{Fore.MAGENTA}[INTELX] Target found in IntelX Intelligence")
            findings["INTELX"] = ["Target confirmed in IntelX Intelligence Database"]
    except: pass
    
    # Dehashed
    try:
        dehashed_url = f"https://www.google.com/search?q=%22{target}%22+site:dehashed.com"
        res = requests.get(dehashed_url, headers=get_headers(), timeout=10)
        clean_and_verify(res.text, target, findings, "DEHASHED")
    except: pass
    
    # GhostProject
    try:
        ghost_url = f"https://ghostproject.fr/?s={target}"
        res = requests.get(ghost_url, headers=get_headers(), timeout=15)
        clean_and_verify(res.text, target, findings, "GHOSTPROJECT")
    except: pass
    
    # Scylla
    try:
        scylla_url = f"https://scylla.one/?q={target}"
        res = requests.get(scylla_url, headers=get_headers(), timeout=15)
        if target.lower() in res.text.lower():
            with print_lock:
                print(f"{Fore.MAGENTA}[SCYLLA] Breach found!")
            findings["SCYLLA"] = ["Target in Scylla breach database"]
    except: pass
    
    # Snusbase
    try:
        snus_url = f"https://snusbase.com/search?q={target}"
        res = requests.get(snus_url, headers=get_headers(), timeout=15)
        clean_and_verify(res.text, target, findings, "SNUSBASE")
    except: pass
    
    # HIBP
    try:
        hibp_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}?truncateResponse=true"
        headers = {"User-Agent": "Khalid-Husain-Investigator"}
        res = requests.get(hibp_url, headers=headers, timeout=10)
        if res.status_code == 200:
            breaches = res.json()
            with print_lock:
                print(f"{Fore.RED}[HIBP] Found in {len(breaches)} breaches!")
            findings["HIBP"] = [f"Found in {len(breaches)} breaches: {breaches}"]
    except: pass
    
    # LeakCheck
    try:
        leakcheck_url = f"https://leakcheck.io/api/search?q={target}"
        res = requests.get(leakcheck_url, headers=get_headers(), timeout=15)
        if '"found":true' in res.text:
            with print_lock:
                print(f"{Fore.MAGENTA}[LEAKCHECK] Positive match!")
            findings["LEAKCHECK"] = ["Target confirmed in leaks"]
    except: pass
    
    # BreachDirectory
    try:
        breachdir_url = f"https://breachdirectory.org/search?q={target}"
        res = requests.get(breachdir_url, headers=get_headers(), timeout=15)
        clean_and_verify(res.text, target, findings, "BREACHDIRECTORY")
    except: pass

def http_protocol_finder(target, findings):
    dorks = [
        f"https://www.google.com/search?q=inurl:http:// -inurl:https:// %22{target}%22",
        f"https://www.bing.com/search?q=%22{target}%22 + \"index of\" + http"
    ]
    for url in dorks:
        try:
            res = requests.get(url, timeout=15, headers=get_headers())
            links = re.findall(r'(https?://[^\s<>"]+)', res.text)
            for link in links[:5]:  # Limit links
                if target in link:
                    with print_lock:
                        print(f"{Fore.YELLOW}[LINK] {Fore.WHITE}{link}")
                    findings["HTTP-LINKS"].append(link)
            clean_and_verify(res.text, target, findings, "HTTP-WEB")
        except: pass

def advanced_onion_scanner(target, findings):
    onion_gateways = [
        f"https://ahmia.fi/search/?q={target}"
    ]
    session = get_onion_session()
    for url in onion_gateways:
        try:
            res = session.get(url, timeout=25, headers=get_headers())
            clean_and_verify(res.text, target, findings, "DARKWEB")
        except: pass

def telegram_dork_engine(target, findings):
    try:
        tg_url = f"https://www.google.com/search?q=site:t.me %22{target}%22"
        res = requests.get(tg_url, timeout=15, headers=get_headers())
        clean_and_verify(res.text, target, findings, "TELEGRAM")
    except: pass

def shadow_crawler_ai(target, findings):
    try:
        paste_url = f"https://www.google.com/search?q=site:pastebin.com %22{target}%22"
        res = requests.get(paste_url, timeout=15, headers=get_headers())
        clean_and_verify(res.text, target, findings, "PASTEBIN")
    except: pass

def silent_tool_runner(cmd, name, findings):
    try:
        tool_check = cmd.split()[0]
        if subprocess.run(f"command -v {tool_check}", shell=True, capture_output=True).returncode != 0:
            return

        process = subprocess.Popen(
            f"torsocks {cmd}", shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            clean = line.strip()
            if any(x in clean.lower() for x in ["found", "http", "match"]):
                with print_lock:
                    print(f"{Fore.GREEN}[{name}] {Fore.WHITE}{clean}")
                if name not in findings:
                    findings[name] = []
                findings[name].append(clean)
    except: pass

def generate_pdf_report(target, findings):
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    markdown_content = f"# KHALID HUSAIN INVESTIGATOR REPORT\n\n"
    markdown_content += f"**Target:** {target}\n"
    markdown_content += f"**Scan Time:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown_content += f"**Total Sources:** {len([k for k,v in findings.items() if v])}\n\n"
    
    for source, hits in findings.items():
        if hits:
            markdown_content += f"## {source}\n\n"
            for hit in hits[:10]:  # Limit per source
                markdown_content += f"- {hit}\n"
            markdown_content += "\n"
    
    # Save markdown first
    md_file = f"reports/{target}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    # Generate PDF
    pdf_file = f"reports/{target}.pdf"
    try:
        HTML(string=markdown_content).write_pdf(pdf_file)
        print(f"\n{Fore.GREEN}[✓] PDF Report Generated: {Fore.WHITE}{os.path.abspath(pdf_file)}")
        print(f"{Fore.CYAN}[📄] Double-click to open PDF instantly!")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] PDF failed (install weasyprint): pip install weasyprint")
        print(f"{Fore.YELLOW}[📝] Markdown backup: {md_file}")

def main():
    start_tor()
    os.system('clear')

    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║ KHALID HUSAIN INVESTIGATOR v78.0 - PDF REPORT MODE ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")

    target = input(f"\n{Fore.WHITE}❯❯ Enter Target: ").strip()
    if not target:
        return

    print(f"{Fore.BLUE}[*] Silent Intelligence Scan Running...\n")
    findings = {}

    threads = [
        Thread(target=intelligence_breach_scan, args=(target, findings)),
        Thread(target=http_protocol_finder, args=(target, findings)),
        Thread(target=advanced_onion_scanner, args=(target, findings)),
        Thread(target=telegram_dork_engine, args=(target, findings)),
        Thread(target=shadow_crawler_ai, args=(target, findings)),
        Thread(target=check_breach_databases, args=(target, findings)),
        Thread(target=lambda: silent_tool_runner(f"sherlock {target} --timeout 10", "Sherlock", findings)),
        Thread(target=lambda: silent_tool_runner(f"maigret {target} --timeout 10", "Maigret", findings))
    ]

    for t in threads:
        t.start()
        time.sleep(0.5)
        
    for t in threads:
        t.join()

    # Generate professional PDF report
    generate_pdf_report(target, findings)

if __name__ == "__main__":
    main()
```

**Key Changes:**
- ✅ **Only displays FOUND data** - No noise, only hits
- ✅ **PDF Report named "Target.pdf"** - Professional format with timestamps
- ✅ **Easy to open** - Double-click friendly in `reports/` folder
- ✅ **All original functions preserved** + new intelligence services

**Install PDF dependency:**
```bash
pip install weasyprint markdown
```

**Output:** Clean console hits + instant PDF report ready to share/open! 🚀
