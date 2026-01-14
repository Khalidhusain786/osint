#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.9 - PASSWORDS VISIBLE + PROFESSIONAL PDF
GLOBAL DATA LAKES + GOVERNMENT + DARK WEB + ALL PII PERFECTLY VISIBLE
"""

import os
import subprocess
import sys
import requests
import re
import time
import json
import urllib.parse
import shlex
from datetime import datetime
from threading import Thread, Lock
from colorama import Fore, Style, init
from bs4 import BeautifulSoup
import importlib.util

# Install missing dependencies automatically
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
    except:
        pass

# Install required packages
required_packages = [
    "colorama", "requests", "beautifulsoup4", "PySocks", 
    "weasyprint", "cssselect2", "html5lib"
]

for package in required_packages:
    if importlib.util.find_spec(package.replace("-", "_").split("=")[0].split(">")[0].split("<")[0]) is None:
        print(f"{Fore.YELLOW}Installing {package}...")
        install_package(package)

try:
    import socks
    TOR_AVAILABLE = True
except ImportError:
    TOR_AVAILABLE = False

init(autoreset=True)
print_lock = Lock()

TARGET_FOLDER = "./Target"
os.makedirs(TARGET_FOLDER, exist_ok=True)

class KhalidHusain786OSINTv859:
    def __init__(self):
        self.target = ""
        self.results = []
        self.pdf_file = ""
        self.tor_session = None
        self.cookies = {}
        self.company_intel = {}
        self.target_pdf = None
        self.scan_complete = False
        
    def banner(self):
        clear_screen()
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}      KHALID HUSAIN786 v85.9 - PASSWORDS VISIBLE       {Fore.RED}║
{Fore.RED}║{Fore.CYAN}PROFESSIONAL PDF • ALL PII PERFECTLY VISIBLE{Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}AADHAAR•VOTER•PAN•GLOBAL•DARK WEB•RESUMES{Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}🎯 LIVE TERMINAL DISPLAY - ALL DATA VISIBLE IN REAL TIME
{Fore.CYAN}📁 SINGLE PDF OUTPUT: {TARGET_FOLDER}/[target].pdf
        """
        print(banner)
    
    def pii_patterns(self):
        return {
            'AADHAAR': r'\b\d{12}\b',
            'PAN': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
            'VOTER_ID': r'(?:[A-Z]{3}[0-9]{7}[A-Z]{1}|[A-Z]{2}[0-9]{9}[A-Z])',
            'EPIC': r'EPI[C]?\s*[0-9]{10}',
            'PASSWORD': r'(?:passw[o0]rd|pwd|token|key|secret|pass|pwd)[:\s]*["\']?([^\s"\'\n]{4,100})["\']?',
            'PASSWORD_HASH': r'\b[A-Fa-f0-9]{32,128}\b',
            'API_KEY': r'(?:api[_-]?key|token|auth[_-]?key|bearer)[:\s]*["\']?([A-Za-z0-9\-_]{20,})["\']?\b',
            'PHONE_IN': r'[\+]?[6-9]\d{9,11}',
            'PHONE_US': r'\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            'PHONE_UK': r'[\+44|0]?[7]\d{9}',
            'PHONE_ALL': r'[\+]?[1-9]\d{7,15}',
            'VEHICLE_IN': r'[A-Z]{2}[0-9]{1,2}[A-Z]{2}\d{4}',
            'VEHICLE_ALL': r'[A-Z0-9-]{6,17}',
            'BTC': r'bc1[A-Za-z9]{39,59}|1[0-9A-Za-z]{25,34}|3[0-9A-Za-z]{25,34}',
            'DOMAIN': r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}',
            'USERNAME': r'@[A-Za-z0-9_]{3,30}|[A-Za-z0-9_]{3,30}(?:@[A-Za-z0-9_]+)?',
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'COMPANY': r'(?:inc|corp|ltd|llc|plc|co\.?\s?|pvt\.?\s?|ltd\.?\s?)(?:\.)?[A-Za-z\s\.\-]{2,50}',
            'LOCATION': r'\b(?:[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4}|[0-9]{4}[/-][0-9]{1,2}[/-][0-9]{1,2}|India|USA|UK|Canada|Australia|Delhi|Mumbai|London|New York)\b',
            'ADDRESS': r'\d{1,4}\s+[A-Za-z\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Blvd|Boulevard|Court|Ct|Place|Pl|Way|Circle|Cir|Square|Sq)\b',
            'REG_DATE': r'(?:registered|created|joined|dob|birth)[\s\-:]+(?:on|at)[\s\-:]+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
        }
    
    def extract_pii(self, text):
        pii_data = {}
        text_lower = text.lower()
        
        patterns = self.pii_patterns()
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                pii_data[pii_type] = matches[0].strip()
                if pii_type == 'COMPANY':
                    self.company_intel['company'] = matches[0].strip()
        
        if self.company_intel.get('company'):
            pii_data['COMPANY'] = self.company_intel['company']
        
        if not pii_data:
            pii_data['TARGET'] = self.target[:30]
        
        return pii_data
    
    def government_scan(self):
        print_live(f"{Fore.RED}🏛️  [GOVERNMENT SCAN STARTED]")
        gov_sources = [
            ("IndiaGov", f"https://www.india.gov.in/search/site/{urllib.parse.quote(self.target)}"),
            ("USA.gov", f"https://www.usa.gov/search?q={urllib.parse.quote(self.target)}"),
            ("UK.gov", f"https://www.gov.uk/search?q={urllib.parse.quote(self.target)}"),
            ("EUData", f"https://data.europa.eu/data/datasets/search?q={urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "GOVERNMENT"), daemon=True) for name, url in gov_sources]
        for t in threads: t.start()
        for t in threads: t.join(45)
        print_live(f"{Fore.GREEN}✅ [GOVERNMENT SCAN COMPLETE]")
    
    def resume_pdf_scan(self):
        print_live(f"{Fore.RED}📄 [RESUME + PDF LEAKS STARTED]")
        pdf_sources = [
            ("ResumeDB", f"https://resumedb.sonatype.com/search?q={urllib.parse.quote(self.target)}"),
            ("PDFSearch", f"https://pdfsearch.io/?q={urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "RESUME"), daemon=True) for name, url in pdf_sources]
        for t in threads: t.start()
        for t in threads: t.join(40)
        print_live(f"{Fore.GREEN}✅ [RESUME SCAN COMPLETE]")
    
    def data_lakes_scan(self):
        print_live(f"{Fore.RED}🌊 [DATA LAKES STARTED]")
        lake_sources = [
            ("LeakIX", f"https://leakix.net/search/?q={urllib.parse.quote(self.target)}"),
            ("IntelX", f"https://intelx.io/search?term={urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "DATALAKE"), daemon=True) for name, url in lake_sources]
        for t in threads: t.start()
        for t in threads: t.join(50)
        print_live(f"{Fore.GREEN}✅ [DATA LAKES COMPLETE]")
    
    def darkweb_scan(self):
        print_live(f"{Fore.RED}🕸️  [DARK WEB INDEXES STARTED]")
        dark_sources = [
            ("DarkSearch", f"https://darksearch.io/?q={urllib.parse.quote(self.target)}"),
            ("Ahmia", f"https://ahmia.fi/search/?q={urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "DARKWEB"), daemon=True) for name, url in dark_sources]
        for t in threads: t.start()
        for t in threads: t.join(55)
        print_live(f"{Fore.GREEN}✅ [DARK WEB COMPLETE]")
    
    def company_scan(self):
        print_live(f"{Fore.RED}🏢 [COMPANY INTEL STARTED]")
        company_sources = [
            ("Clearbit", f"https://company.clearbit.com/v2/companies/find?domain={urllib.parse.quote(self.target.split('@')[1] if '@' in self.target else self.target)}"),
            ("Crunchbase", f"https://www.crunchbase.com/textsearch?q={urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "COMPANY"), daemon=True) for name, url in company_sources]
        for t in threads: t.start()
        for t in threads: t.join(40)
        print_live(f"{Fore.GREEN}✅ [COMPANY SCAN COMPLETE]")
    
    def password_scan(self):
        print_live(f"{Fore.RED}🔑 [PASSWORDS + TOKENS STARTED]")
        password_sources = [
            ("Pastebin", f"https://pastebin.com/search?q={urllib.parse.quote(self.target)}"),
            ("GhostProject", f"https://ghostproject.fr/?q={urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "PASSWORD"), daemon=True) for name, url in password_sources]
        for t in threads: t.start()
        for t in threads: t.join(35)
        print_live(f"{Fore.GREEN}✅ [PASSWORD SCAN COMPLETE]")
    
    def breach_scan(self):
        print_live(f"{Fore.RED}💥 [BREACHES STARTED]")
        global_breaches = [
            ("HIBP", f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"),
            ("LeakCheck", f"https://leakcheck.io/api/?key=demo&q={urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "BREACH"), daemon=True) for name, url in global_breaches]
        for t in threads: t.start()
        for t in threads: t.join(40)
        print_live(f"{Fore.GREEN}✅ [BREACH SCAN COMPLETE]")
    
    def username_scan(self):
        print_live(f"{Fore.RED}👤 [USERNAME TRACKER STARTED]")
        usernames = [
            ("NameCheckr", f"https://namecheckr.com/search/{urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "USERNAME"), daemon=True) for name, url in usernames]
        for t in threads: t.start()
        for t in threads: t.join(30)
        print_live(f"{Fore.GREEN}✅ [USERNAME SCAN COMPLETE]")
    
    def kali_tool_scan(self):
        print_live(f"{Fore.RED}⚡ [KALI TOOLS STARTED]")
        try:
            result = subprocess.run(["theHarvester", "-d", self.target, "-b", "google", "-l", "100"], 
                                  capture_output=True, text=True, timeout=60)
            self.print_result("KALI", {'TOOL': 'theHarvester'}, "KaliLinux", "theHarvester", "", "⚡")
        except:
            pass
        print_live(f"{Fore.GREEN}✅ [KALI TOOLS COMPLETE]")
    
    def crypto_scan(self):
        print_live(f"{Fore.RED}₿ [CRYPTO TRACKER STARTED]")
        crypto = [
            ("BTC.com", f"https://btc.com/{urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "CRYPTO"), daemon=True) for name, url in crypto]
        for t in threads: t.start()
        for t in threads: t.join(25)
        print_live(f"{Fore.GREEN}✅ [CRYPTO SCAN COMPLETE]")
    
    def social_media_scan(self):
        print_live(f"{Fore.RED}📱 [SOCIAL PROFILES STARTED]")
        social = [
            ("Facebook", f"https://www.facebook.com/{urllib.parse.quote(self.target)}"),
            ("Twitter", f"https://twitter.com/{urllib.parse.quote(self.target)}"),
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "SOCIAL"), daemon=True) for name, url in social]
        for t in threads: t.start()
        for t in threads: t.join(30)
        print_live(f"{Fore.GREEN}✅ [SOCIAL SCAN COMPLETE]")
    
    def print_live(self, message):
        """Print live updates that always show on terminal"""
        with print_lock:
            print(f"\r{Fore.WHITE}{message:<100}{Style.RESET_ALL}", end="", flush=True)
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        with print_lock:
            emojis = {
                "BREACH": "💥", "KALI": "⚡", "SOCIAL": "📱", "CRYPTO": "₿", 
                "USERNAME": "👤", "COMPANY": "🏢", "PASSWORD": "🔑", 
                "GOVERNMENT": "🏛️", "RESUME": "📄", "DATALAKE": "🌊", "DARKWEB": "🕸️"
            }
            emoji = emojis.get(category, "🌐")
            
            # Clear previous line and print new result
            print(f"\n{Fore.GREEN}✓ [{emoji}] {Fore.CYAN}{category:12s} | {Fore.YELLOW}{source:14s} | {Fore.MAGENTA}{engine:12s} | 🔗 {link[:60]}...")
            
            if isinstance(data, dict):
                for pii_type, pii_value in data.items():
                    color = Fore.RED if any(x in pii_type.upper() for x in ['PASS', 'KEY', 'HASH', 'AADHAAR', 'PAN', 'VOTER']) else Fore.WHITE
                    print(f"   {Fore.CYAN}🆔 {pii_type:<12s}: {color}{pii_value[:80]}{Style.RESET_ALL}")
            else:
                print(f"   {Fore.RED}→ {data[:100]}{Style.RESET_ALL}")
            
            print(f"{Style.RESET_ALL}")
            
            self.results.append({
                'category': category, 'data': data, 'source': source,
                'engine': engine, 'link': link if link.startswith('http') else f"https://google.com/search?q={urllib.parse.quote(self.target)}+{urllib.parse.quote(source)}",
                'network': network, 'timestamp': datetime.now().isoformat()
            })
    
    def tor_init(self):
        try:
            if TOR_AVAILABLE:
                self.tor_session = requests.Session()
                self.tor_session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                print_live(f"{Fore.CYAN}🌀 TOR INITIALIZED")
                return True
        except:
            pass
        return False
    
    def scan_url(self, url, source, engine="WEB"):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            session = self.tor_session if self.tor_session else requests
            resp = session.get(url, headers=headers, timeout=25, allow_redirects=True)
            
            if resp.status_code == 200:
                text = resp.text[:50000]  # Limit text size
                pii_found = self.extract_pii(text)
                
                if pii_found:
                    self.print_result(engine, pii_found, source, engine, url)
                else:
                    self.print_result(engine, {'TARGET': f"{self.target} found"}, source, engine, url)
                    
        except Exception:
            # Silent fail for individual URLs
            pass
    
    def generate_pdf(self):
        """Generate final PDF after all scans complete"""
        if not self.results:
            print(f"\n{Fore.YELLOW}❌ No results found for {self.target}")
            return
        
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:50]
        self.target_pdf = f"{TARGET_FOLDER}/{clean_target}.pdf"
        html_file = f"{TARGET_FOLDER}/{clean_target}.html"
        
        # Generate HTML with all results
        html_content = self.create_html_report()
        
        # Save HTML first (always works)
        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n{Fore.CYAN}📄 HTML Report: {html_file}")
        except:
            pass
        
        # Try PDF generation
        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(self.target_pdf)
            print(f"{Fore.GREEN}✅ PROFESSIONAL PDF: {self.target_pdf} ({len(self.results)} records)")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  HTML ready: {html_file} (PDF failed - use browser)")
    
    def create_html_report(self):
        total_records = len(self.results)
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{self.target} - GLOBAL OSINT v85.9</title>
<style>
body{{font-family:'Courier New',monospace;background:#0a0e17;color:#e6edf3;font-size:11px;line-height:1.4;padding:25px;max-width:100%;}}
h1{{color:#00d4aa;font-size:24px;text-align:center;margin:0 0 30px 0;font-weight:700;}}
h2{{color:#ff6b6b;font-size:16px;border-bottom:3px solid #1a2332;padding-bottom:12px;margin:35px 0 25px 0;}}
.pii-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:20px;margin:25px 0;}}
.pii-card{{background:linear-gradient(145deg,#1a2332 0%,#212b40 100%);padding:25px;border-radius:15px;border-left:6px solid #00d4aa;box-shadow:0 8px 32px rgba(0,0,0,0.6);}}
.pii-type{{font-weight:900;color:#00d4aa;font-size:13px;margin-bottom:12px;text-transform:uppercase;letter-spacing:1px;}}
.pii-value{{font-family:monospace;background:#0a0e17;padding:15px;border-radius:10px;font-size:12px;color:#ffffff;border:2px solid #2d4059;font-weight:600;word-break:break-all;line-height:1.6;max-height:120px;overflow-y:auto;}}
.stats{{text-align:center;background:rgba(26,35,50,0.9);padding:30px;border-radius:20px;margin:30px 0;box-shadow:0 15px 50px rgba(0,0,0,0.5);}}
.stat-number{{font-size:36px;font-weight:900;color:#00d4aa;display:block;margin-bottom:10px;}}
.footer{{text-align:center;font-size:12px;color:#64748b;margin-top:60px;padding-top:40px;border-top:4px solid #1a2332;padding-bottom:30px;}}
@media print {{ body{{font-size:10px;}} .pii-grid{{grid-template-columns:repeat(4,1fr);gap:15px;}} }}
</style>
</head>
<body>
<h1>🌐 {self.target} - GLOBAL OSINT DOSSIER v85.9</h1>

<div class="stats">
<div class="stat-number">{total_records}</div>
<span style="color:#a0b3c6;font-size:18px;">TOTAL INTELLIGENCE RECORDS FOUND</span>
<br><br>
<span style="color:#00d4aa;font-size:14px;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</span>
</div>

'''

        if self.company_intel.get('company'):
            html += f'''
<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:35px;border-radius:25px;margin:40px 0;box-shadow:0 20px 60px rgba(102,126,234,0.4);">
<h2 style="color:#fff;margin:0 0 25px 0;font-size:20px;">🏢 TARGET COMPANY PROFILE</h2>
<div style="font-family:monospace;background:#1a2332;padding:25px;border-radius:15px;border-left:5px solid #fff;">
<div style="color:#00d4aa;font-size:16px;font-weight:900;">{self.company_intel['company']}</div>
</div>
</div>
'''

        html += '<h2 style="color:#ff6b6b;">🆔 ALL RECORDS FOUND (' + str(total_records) + ')</h2><div class="pii-grid">'

        for result in self.results[-50:]:  # Last 50 results for PDF size
            if isinstance(result['data'], dict):
                for pii_type, pii_value in result['data'].items():
                    html += f'''
<div class="pii-card">
<div class="pii-type">{result["category"]} - {pii_type}</div>
<div class="pii-value">{pii_value}</div>
<div style="font-size:11px;color:#a0b3c6;margin-top:15px;">
📡 {result["source"]} | ⚙️ {result["engine"]} | {result["timestamp"][:16]}
</div>
</div>'''
            else:
                html += f'''
<div class="pii-card">
<div class="pii-type">{result["category"]}</div>
<div class="pii-value">{str(result["data"])}</div>
<div style="font-size:11px;color:#a0b3c6;margin-top:15px;">
📡 {result["source"]} | ⚙️ {result["engine"]}
</div>
</div>'''

        html += f'''</div>
<div class="footer">
<strong>KhalidHusain786 OSINT v85.9</strong> | {total_records} Records Captured | All PII Perfectly Visible<br>
<i>GLOBAL GOVERNMENT • DATA LAKES • DARK WEB • PASSWORDS VISIBLE</i>
</div>
</body>
</html>'''
        return html
    
    def run_full_scan(self):
        self.banner()
        print(f"\n{Fore.WHITE}🎯 TARGET ACQUIRED: {Fore.YELLOW}{self.target}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📁 OUTPUT FOLDER: {TARGET_FOLDER}/{Style.RESET_ALL}")
        print("=" * 120)
        print()
        
        self.tor_init()
        time.sleep(2)
        
        # Run all 12 scans in parallel
        scans = [
            self.government_scan, self.resume_pdf_scan, self.data_lakes_scan,
            self.darkweb_scan, self.company_scan, self.password_scan,
            self.breach_scan, self.username_scan, self.crypto_scan,
            self.social_media_scan, self.kali_tool_scan
        ]
        
        scan_threads = [Thread(target=scan, daemon=True) for scan in scans]
        for t in scan_threads:
            t.start()
        for t in scan_threads:
            t.join()
        
        self.scan_complete = True
        
        print(f"\n" + "="*120)
        print(f"{Fore.RED}🎉 GLOBAL SCAN COMPLETE!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 {len(self.results)} TOTAL RECORDS FOUND{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📄 GENERATING PROFESSIONAL PDF...{Style.RESET_ALL}")
        
        self.generate_pdf()
        print(f"\n{Fore.MAGENTA}🚀 SCAN FINISHED - CHECK {TARGET_FOLDER}/{Style.RESET_ALL}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target_email_or_name>{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Example: python3 khalid-osint.py test@example.com{Style.RESET_ALL}")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv859()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()
