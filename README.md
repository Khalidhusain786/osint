<h1 align="center">🕵️‍♂️ KHALID HYBRID OSINT ENGINE</h1>
<p align="center">
<b>Surface + Deep + Dark Recon • Telegram • Data Breaches • Onion Spider • Identity Extractor</b>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Recon-OSINT-blue?style=for-the-badge">
<img src="https://img.shields.io/badge/Mode-HYBRID-orange?style=for-the-badge">
<img src="https://img.shields.io/badge/Tor-AUTO-green?style=for-the-badge">
<img src="https://img.shields.io/badge/Report-TXT%2FPDF-yellow?style=for-the-badge">
<img src="https://img.shields.io/badge/Platform-Kali%20%7C%20Ubuntu%20%7C%20Termux-red?style=for-the-badge">
</p>

---

## 🚀 **About The Engine**

> **Khalid Hybrid OSINT Engine** is a full-spectrum recon suite that performs:
✔ Surface Web  
✔ Deep Web  
✔ Dark Web  
✔ Telegram Dorks  
✔ Leak Databases  
✔ Identity Extraction  
✔ Breach Checks  
✔ Final Reports  

All through one unified pipeline.

---

## 🧬 **Core Abilities**

✔ Automatic TOR routing (No manual start)  
✔ Deep + Dark onion spider gateways  
✔ Telegram intelligence dorks  
✔ Leak databases enumeration  
✔ Data breach hunter  
✔ WHOIS & platform lookups  
✔ Entity Identity Classification (PAN, Aadhaar, Phone, Address etc.)  
✔ PDF & TXT reporting  
✔ Artifact link retention  
✔ Colorized output  
✔ Threaded high-speed mode  

---

## 🔍 **Supported Targets**

```
Name
Email
Phone
PAN
Aadhaar
Voter ID
Domain
Username
Address Patterns
Bitcoin Wallets
IP & Network
```

---

## 🧩 **Recon Modules**

| Module | Layer |
|---|---|
| HTTP Dorks | Surface |
| Telegram Dorks | Semi-Deep |
| Pastebin/Leak Dumps | Deep |
| Onion Spider | Deep/Dark |
| Breach Check | LeakNet |
| Sherlock | Surface OSINT |
| Maigret | Aggregated OSINT |
| Identity Extraction | NLP |
| PDF Builder | Reporting |
| Tor Router | Transport |

---

## 🛠 **Installation**

### **Kali / Ubuntu / Parrot / Debian**

```bash
cd /home/kali && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && chmod +x install.sh && sudo ./install.sh && sudo ln -sf $(which maigret || echo "$HOME/.local/bin/maigret") /usr/bin/maigret && sudo service tor restart && clear && python3 khalid-osint.py
```

### **Termux**

```bash
pkg update -y && pkg upgrade -y && pkg install python git tor torsocks libxml2 libxslt -y || sudo apt update -y && sudo apt install python3 python3-pip tor torsocks git libxml2-dev libxslt-dev -y; pip install colorama requests beautifulsoup4 lxml urllib3 sherlock maigret; (tor > /dev/null 2>&1 &); python khalid-osint.pyimport os, subprocess, sys, requests, re, time, random
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
    print(f"{Fore.GREEN}[OK] Ghost Tunnel: HTTP/HTTPS/ONION PROTOCOLS ACTIVE")

def clean_and_verify(raw_html, target, report_file, source_label):
    try:
        # Fallback if lxml is missing
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
                with print_lock:
                    print(f"{Fore.RED}[{source_label}-HIT] {Fore.WHITE}{clean_line}")
                with open(report_file, "a") as f:
                    f.write(f"[{source_label}] {clean_line}\n")
    except:
        pass

def check_breach_databases(target, report_file):
    try:
        if "@" in target:
            res = requests.get(
                f"https://www.google.com/search?q=%22{target}%22+site:leak-lookup.com+OR+site:intelx.io",
                headers=get_headers()
            )
            clean_and_verify(res.text, target, report_file, "BREACH-INFO")
    except:
        pass

def http_protocol_finder(target, report_file):
    dorks = [
        f"https://www.google.com/search?q=inurl:http:// -inurl:https:// %22{target}%22",
        f"https://www.bing.com/search?q=%22{target}%22 + \"index of\" + http",
        f"https://yandex.com/search/?text=site:*.in %22{target}%22"
    ]
    for url in dorks:
        try:
            res = requests.get(url, timeout=15, headers=get_headers())
            links = re.findall(r'(https?://[^\s<>"]+|[a-z2-7]{56}\.onion)', res.text)
            for link in links:
                if target in link:
                    with print_lock:
                        print(f"{Fore.YELLOW}[LINK-FOUND] {Fore.WHITE}{link}")
            clean_and_verify(res.text, target, report_file, "HTTP-WEB")
        except:
            pass

def advanced_onion_scanner(target, report_file):
    onion_gateways = [
        f"http://jnv3gv3yuvpwhv7y.onion/search/?q={target}",
        f"https://ahmia.fi/search/?q={target}",
        f"http://phishsetvsnm4v5n.onion/search.php?q={target}"
    ]
    session = get_onion_session()
    for url in onion_gateways:
        try:
            res = session.get(url, timeout=25, headers=get_headers())
            clean_and_verify(res.text, target, report_file, "DARK-DEEP")
        except:
            pass

def telegram_dork_engine(target, report_file):
    tg_links = [
        f"https://www.google.com/search?q=site:t.me OR site:telegram.me %22{target}%22",
        f"https://yandex.com/search/?text=%22{target}%22 site:t.me"
    ]
    for url in tg_links:
        try:
            res = requests.get(url, timeout=15, headers=get_headers())
            clean_and_verify(res.text, target, report_file, "TG-DATA")
        except:
            pass

def shadow_crawler_ai(target, report_file):
    gateways = [
        f"https://psbdmp.ws/api/search/{target}",
        f"https://www.google.com/search?q=site:pastebin.com OR site:ghostbin.co OR site:controlc.com %22{target}%22"
    ]
    for url in gateways:
        try:
            res = requests.get(url, timeout=15, headers=get_headers())
            clean_and_verify(res.text, target, report_file, "LEAK-DB")
        except:
            pass

def silent_tool_runner(cmd, name, report_file):
    try:
        # Verify if tool is installed before execution
        tool_check = cmd.split()[0]
        if subprocess.run(f"command -v {tool_check}", shell=True, capture_output=True).returncode != 0:
            with print_lock:
                print(f"{Fore.YELLOW}[!] {name} not found in system. Skipping...")
            return

        process = subprocess.Popen(
            f"torsocks {cmd}", shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in process.stdout:
            clean = line.strip()
            if any(x in clean.lower() for x in ["http", "found", "match:", "onion"]):
                with print_lock:
                    print(f"{Fore.GREEN}[{name.upper()}-HIT] {Fore.WHITE}{clean}")
                with open(report_file, "a") as f:
                    f.write(f"[{name}] {clean}\n")
    except:
        pass

def main():
    if not os.path.exists('reports'):
        os.makedirs('reports')

    start_tor()
    os.system('clear')

    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║ KHALID HUSAIN INVESTIGATOR - UNIVERSAL PROTOCOL v76.0 ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")

    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/PAN/ID): ")
    if not target:
        return

    report_path = os.path.abspath(f"reports/{target}.txt")
    if os.path.exists(report_path):
        os.remove(report_path)

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

    for t in threads:
        t.start()
        time.sleep(1) # Chhota gap rate limiting se bachne ke liye
        
    for t in threads:
        t.join()

    print(f"\n{Fore.GREEN}[➔] Investigation Complete. Comprehensive Report: {report_path}")

if __name__ == "__main__":
    main()
```

---

## ▶ **Run**

Direct launch:

```bash
python3 khalid-osint.py
```

---

## 🎛 **AUTO-TOR Mode**

✔ Automatically starts TOR  
✔ Applies onion socks proxy  
✔ No manual config required  

---

## 📁 **Folder Layout**

```
osint/
 ├─ khalid-osint.py
 ├─ install.sh
 ├─ requirements.txt
 ├─ api_keys.json
 ├─ reports/
 ├─ assets/
 │   └─ banner.png
 └─ screenshots/
```

---

## 📜 **Report Output**

Formats:

```
/reports/<target>.txt
/reports/<target>.pdf
```

Includes:

✔ Found Data  
✔ Sources  
✔ Dork hits  
✔ Onion links  
✔ Platform profiles  
✔ Evidence chain  

---

## 📸 **Screenshots**

```
screenshots/terminal.png
screenshots/report.png
```

(Will be auto added)

---

## 🔑 **Optional API Keys**

`api_keys.json`

```json
{
  "truecaller": "",
  "hunter": "",
  "email_hippo": "",
  "hlr_lookup": ""
}
```

---

## ⚡ Performance Notes

✔ Multi-threaded  
✔ Proxy aware  
✔ Timeout hardened  
✔ Onion fallback  
✔ Leak redundancy  

---

## 🧾 **Legal Notice**

> This tool is intended for **education + investigative OSINT** only.  
> User assumes all liability.  
> Do not violate privacy or local laws.

---

## 👑 **Author**

**Developer:** `Khalid Husain`  
**Engine:** `Hybrid Recon AI v1`

---

## 📜 **License**

```
MIT License
```

---

## ⭐ **Give it a Star**

If this helps your work, star the repo 🙂```

---

## 🖥️ Output Preview

> **Minimal Terminal Output (Only Hits)**

```
[DARK-DEEP] Passport leak found
[TG-DATA] Mention detected: @username
[BREACH] Email found in 4 breaches
[LINK] https://example.onion
[REPORT] Saved → /reports/target.pdf
```

---

## 📑 Report System

Export options:

✔ Terminal Hits  
✔ PDF Report  
✔ TXT Raw  

All reports auto-saved using:

```
{target}/{target_report}.pdf
```

---

## 🔑 API Keys (Optional)

Place in:

```
config/api_keys.json
```

Supported:

- truecaller
- hunter
- emailhippo
- hlr lookup

---

## 📱 Platforms Supported

✔ Kali Linux  
✔ Ubuntu / Debian  
✔ Parrot OS  
✔ Termux (Android)  
✔ VPS / Cloud / Local

---

## ⚖️ Legal Disclaimer

This project is for **OSINT & Educational Forensics** only.  
User is responsible for usage compliant with law & jurisdiction.

---

## 👑 Credits

Author: **Khalid Husain**  
Engine: **Hybrid OSINT Recon**

---

## 📜 License

MIT License (safe for public use & fork)

---

## 🗺️ Roadmap (Future)

- Browser Fingerprint Recon
- Telegram Bots Integration
- Full GUI Panel
- Auto Enrichment
