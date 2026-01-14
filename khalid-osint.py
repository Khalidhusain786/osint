#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.8 - GLOBAL DATA LAKES + DEEP/DARK WEB + GOVERNMENT + ALL PII
ALL SOURCES • AADHAAR • VOTER ID • PAN • GLOBAL PHONES • RESUMES • PDF LEAKS • BREACHES
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
try:
    import socks
    TOR_AVAILABLE = True
except ImportError:
    TOR_AVAILABLE = False

init(autoreset=True)
print_lock = Lock()

TARGET_FOLDER = "./Target"
os.makedirs(TARGET_FOLDER, exist_ok=True)

class KhalidHusain786OSINTv857:
    def __init__(self):
        self.target = ""
        self.results = []
        self.pdf_file = ""
        self.tor_session = None
        self.cookies = {}
        self.company_intel = {}
        self.target_pdf = None  # SINGLE PDF ONLY
        
    def banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}      KHALID HUSAIN786 v85.8 - GLOBAL DATA LAKES      {Fore.RED}║
{Fore.RED}║{Fore.CYAN}DARK WEB•DEEP WEB•GOV•AADHAAR•VOTER•PAN•ALL PII{Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}RESUMES•PDF LEAKS•DATA BREACHES•WORLDWIDE{Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def pii_patterns(self):
        return {
            # INDIA GOVERNMENT ID's
            'AADHAAR': r'\b\d{12}\b',
            'PAN': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
            'VOTER_ID': r'(?:[A-Z]{3}[0-9]{7}[A-Z]{1}|[A-Z]{2}[0-9]{9}[A-Z])',
            'EPIC': r'EPI[C]?\s*[0-9]{10}',
            
            # PASSWORDS & TOKENS
            'PASSWORD': r'(?:passw[o0]rd|pwd|token|key|secret|pass|pwd)[:\s]*["\']?([^\s"\'\n]{4,100})["\']?',
            'PASSWORD_HASH': r'\b[A-Fa-f0-9]{32,128}\b',
            'API_KEY': r'(?:api[_-]?key|token|auth[_-]?key|bearer)[:\s]*["\']?([A-Za-z0-9\-_]{20,})["\']?\b',
            
            # GLOBAL PHONES
            'PHONE_IN': r'[\+]?[6-9]\d{9,11}',
            'PHONE_US': r'\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            'PHONE_UK': r'[\+44|0]?[7]\d{9}',
            'PHONE_ALL': r'[\+]?[1-9]\d{7,15}',
            
            # VEHICLE & CRYPTO
            'VEHICLE_IN': r'[A-Z]{2}[0-9]{1,2}[A-Z]{2}\d{4}',
            'VEHICLE_ALL': r'[A-Z0-9-]{6,17}',
            'BTC': r'bc1[A-Za-z9]{39,59}|1[0-9A-Za-z]{25,34}|3[0-9A-Za-z]{25,34}',
            
            # DIGITAL FOOTPRINT
            'DOMAIN': r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}',
            'USERNAME': r'@[A-Za-z0-9_]{3,30}|[A-Za-z0-9_]{3,30}(?:@[A-Za-z0-9_]+)?',
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            
            # COMPANY & LOCATION
            'COMPANY': r'(?:inc|corp|ltd|llc|plc|co\.?\s?|pvt\.?\s?|ltd\.?\s?)(?:\.)?[A-Za-z\s\.\-]{2,50}',
            'LOCATION': r'\b(?:[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4}|[0-9]{4}[/-][0-9]{1,2}[/-][0-9]{1,2}|India|USA|UK|Canada|Australia|Delhi|Mumbai|London|New York)\b',
            'ADDRESS': r'\d{1,4}\s+[A-Za-z\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Blvd|Boulevard|Court|Ct|Place|Pl|Way|Circle|Cir|Square|Sq)\b',
            
            # DATES
            'REG_DATE': r'(?:registered|created|joined|dob|birth)[\s\-:]+(?:on|at)[\s\-:]+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
        }
    
    def extract_pii(self, text):
        pii_data = {}
        text_lower = text.lower()
        
        patterns = self.pii_patterns()
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                full_match = matches[0]
                if pii_type == 'COMPANY' and full_match:
                    self.company_intel['company'] = full_match.strip()
                pii_data[pii_type] = full_match.strip()  # FULL data preserved
        
        if self.company_intel.get('company'):
            pii_data['COMPANY'] = self.company_intel['company']
        
        if not pii_data:
            pii_data['TARGET'] = self.target[:30]
        
        return pii_data
    
    # NEW: GLOBAL GOVERNMENT & DATA LAKES
    def government_scan(self):
        print(f"{Fore.RED}🏛️  GOVERNMENT + PUBLIC RECORDS")
        gov_sources = [
            ("IndiaGov", f"https://www.india.gov.in/search/site/{urllib.parse.quote(self.target)}"),
            ("USA.gov", f"https://www.usa.gov/search?q={urllib.parse.quote(self.target)}"),
            ("UK.gov", f"https://www.gov.uk/search?q={urllib.parse.quote(self.target)}"),
            ("EUData", f"https://data.europa.eu/data/datasets/search?q={urllib.parse.quote(self.target)}"),
            ("IndiaUIDAI", f"https://uidai.gov.in/images/commdoc/aadhaar_data_retention_policy.pdf"),
            ("VoterIndia", f"https://electoralsearch.eci.gov.in/search"),
            ("PANIndia", f"https://www.incometax.gov.in/iec/foportal/"),
            ("CanadaGov", f"https://open.canada.ca/en/search/site/{urllib.parse.quote(self.target)}"),
            ("AusGov", f"https://data.gov.au/dataset?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "GOVERNMENT"), daemon=True) for name, url in gov_sources]
        for t in threads: t.start()
        for t in threads: t.join(45)
    
    # NEW: RESUMES & PDF LEAKS
    def resume_pdf_scan(self):
        print(f"{Fore.RED}📄 RESUMES + PDF LEAKS")
        pdf_sources = [
            ("ResumeDB", f"https://resumedb.sonatype.com/search?q={urllib.parse.quote(self.target)}"),
            ("PDFSearch", f"https://pdfsearch.io/?q={urllib.parse.quote(self.target)}"),
            ("GitHubPDF", f"https://github.com/search?q={urllib.parse.quote(self.target)}+filename:resume+OR+cv+OR+filetype:pdf"),
            ("Scribd", f"https://www.scribd.com/search-documents?query={urllib.parse.quote(self.target)}"),
            ("SlideShare", f"https://www.slideshare.net/search/slideshow?searchfrom=header&q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "RESUME"), daemon=True) for name, url in pdf_sources]
        for t in threads: t.start()
        for t in threads: t.join(40)
    
    # NEW: DATA LAKES & DEEP WEB
    def data_lakes_scan(self):
        print(f"{Fore.RED}🌊 DATA LAKES + DEEP WEB")
        lake_sources = [
            ("LeakIX", f"https://leakix.net/search/?q={urllib.parse.quote(self.target)}"),
            ("IntelX", f"https://intelx.io/search?term={urllib.parse.quote(self.target)}"),
            ("DataBreaches", f"https://databreaches.net/?s={urllib.parse.quote(self.target)}"),
            ("ExploitDB", f"https://www.exploit-db.com/search?q={urllib.parse.quote(self.target)}"),
            ("VirusTotal", f"https://www.virustotal.com/gui/search/{urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "DATALAKE"), daemon=True) for name, url in lake_sources]
        for t in threads: t.start()
        for t in threads: t.join(50)
    
    # NEW: DARK WEB + TOR INDEXES (Surface accessible)
    def darkweb_scan(self):
        print(f"{Fore.RED}🕸️  DARK WEB INDEXES")
        dark_sources = [
            ("DarkSearch", f"https://darksearch.io/?q={urllib.parse.quote(self.target)}"),
            ("Ahmia", f"https://ahmia.fi/search/?q={urllib.parse.quote(self.target)}"),
            ("TorSearch", f"https://torsearch.io/search/?q={urllib.parse.quote(self.target)}"),
            ("OnionDir", f"https://www.oniondir.biz/search/?q={urllib.parse.quote(self.target)}"),
            ("FreshOnions", f"https://www.freshonions.torri.ng/search/?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "DARKWEB"), daemon=True) for name, url in dark_sources]
        for t in threads: t.start()
        for t in threads: t.join(55)
    
    # EXISTING SCANS (unchanged)
    def company_scan(self):
        print(f"{Fore.RED}🏢 COMPANY INTEL")
        company_sources = [
            ("Clearbit", f"https://company.clearbit.com/v2/companies/find?domain={urllib.parse.quote(self.target.split('@')[1] if '@' in self.target else self.target)}"),
            ("Crunchbase", f"https://www.crunchbase.com/textsearch?q={urllib.parse.quote(self.target)}"),
            ("Hunter", f"https://hunter.io/search/{urllib.parse.quote(self.target)}"),
            ("OpenCorp", f"https://opencorporates.com/search?q={urllib.parse.quote(self.target)}"),
            ("SEC", f"https://www.sec.gov/edgar/search/#/q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "COMPANY"), daemon=True) for name, url in company_sources]
        for t in threads: t.start()
        for t in threads: t.join(40)
    
    def password_scan(self):
        print(f"{Fore.RED}🔑 PASSWORDS + TOKENS")
        password_sources = [
            ("Pastebin", f"https://pastebin.com/search?q={urllib.parse.quote(self.target)}"),
            ("GhostProject", f"https://ghostproject.fr/?q={urllib.parse.quote(self.target)}"),
            ("PasteHunt", f"https://paste.hunt.io/?q={urllib.parse.quote(self.target)}"),
            ("Hashmob", f"https://hashmob.net/search?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "PASSWORD"), daemon=True) for name, url in password_sources]
        for t in threads: t.start()
        for t in threads: t.join(35)
    
    def breach_scan(self):
        print(f"{Fore.RED}💥 BREACHES + PASSWORDS")
        global_breaches = [
            ("HIBP", f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"),
            ("DeHashed", f"https://dehashed.com/search?query={urllib.parse.quote(self.target)}"),
            ("LeakCheck", f"https://leakcheck.io/api/?key=demo&q={urllib.parse.quote(self.target)}"),
            ("BreachDir", f"https://breachdirectory.org/search?email={urllib.parse.quote(self.target)}"),
            ("Snusbase", f"https://snusbase.com/search?q={urllib.parse.quote(self.target)}"),
            ("WeLeakInfo", f"https://weleakinfo.to/?search={urllib.parse.quote(self.target)}"),
            ("LeakDB", f"https://leakdb.abyss.sh/?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "BREACH"), daemon=True) for name, url in global_breaches]
        for t in threads: t.start()
        for t in threads: t.join(40)
    
    def username_scan(self):
        print(f"{Fore.RED}👤 USERNAME TRACKER")
        usernames = [
            ("NameCheckr", f"https://namecheckr.com/search/{urllib.parse.quote(self.target)}"),
            ("KnowEm", f"https://knowem.com/checkusernames.php?u={urllib.parse.quote(self.target)}"),
            ("Namecheap", f"https://www.namecheap.com/domains/registration/results/?domain={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "USERNAME"), daemon=True) for name, url in usernames]
        for t in threads: t.start()
        for t in threads: t.join(30)
    
    def kali_tool_scan(self):
        print(f"{Fore.RED}⚡ KALI TOOLS")
        kali_tools = [
            ("theHarvester", ["theHarvester", "-d", self.target, "-b", "all", "-l", "500"]),
            ("dnsdumpster", f"https://dnsdumpster.com/?target={urllib.parse.quote(self.target)}"),
            ("Shodan", f"https://www.shodan.io/search?query={urllib.parse.quote(self.target)}")
        ]
        for tool_name, cmd_or_url in kali_tools:
            if isinstance(cmd_or_url, list):
                try:
                    result = subprocess.run(cmd_or_url, capture_output=True, text=True, timeout=300)
                    self.print_result("KALI", f"{self.target} | {tool_name}", "Kali", tool_name, "", "⚡")
                except: pass
            else:
                self.scan_url(cmd_or_url, tool_name, "KALI")
    
    def crypto_scan(self):
        print(f"{Fore.RED}₿ CRYPTO TRACKER")
        crypto = [
            ("BTC.com", f"https://btc.com/{urllib.parse.quote(self.target)}"),
            ("Blockchain", f"https://www.blockchain.com/explorer/search?search={urllib.parse.quote(self.target)}"),
            ("Etherscan", f"https://etherscan.io/search?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "CRYPTO"), daemon=True) for name, url in crypto]
        for t in threads: t.start()
        for t in threads: t.join(25)
    
    def social_media_scan(self):
        print(f"{Fore.RED}📱 SOCIAL PROFILES")
        social = [
            ("Facebook", f"https://www.facebook.com/{urllib.parse.quote(self.target)}"),
            ("Twitter", f"https://twitter.com/{urllib.parse.quote(self.target)}"),
            ("Instagram", f"https://www.instagram.com/{urllib.parse.quote(self.target)}"),
            ("GitHub", f"https://github.com/{urllib.parse.quote(self.target)}"),
            ("LinkedIn", f"https://www.linkedin.com/in/{urllib.parse.quote(self.target.replace('@',''))}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "SOCIAL"), daemon=True) for name, url in social]
        for t in threads: t.start()
        for t in threads: t.join(30)
    
    def update_pdf(self):
        if not self.results:
            return
        
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:50]
        self.target_pdf = f"{TARGET_FOLDER}/{clean_target}.pdf"
        
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{self.target} - GLOBAL OSINT v85.8</title>
<style>
body{{font-family:'Courier New',monospace;background:#0a0e17;color:#e6edf3;font-size:9px;line-height:1.25;padding:25px;max-width:100%;margin:0;overflow:hidden;}}
h1{{color:#00d4aa;font-size:20px;text-align:center;margin:0 0 30px 0;font-weight:700;text-shadow:0 0 15px rgba(0,212,170,0.6);}}
h2{{color:#ff6b6b;font-size:13px;border-bottom:2px solid #1a2332;padding-bottom:10px;margin:30px 0 20px 0;letter-spacing:1px;}}
.stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin:25px 0;background:rgba(26,35,50,0.9);padding:25px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,0.4);}}
.stat-card{{text-align:center;padding:20px;background:linear-gradient(135deg,#1a2332 0%,#2d4059 100%);border-radius:12px;border:2px solid #00d4aa;box-shadow:0 6px 25px rgba(0,212,170,0.15);}}
.stat-number{{font-size:28px;font-weight:900;color:#00d4aa;margin-bottom:8px;text-shadow:0 0 10px rgba(0,212,170,0.5);}}
.stat-label{{font-size:11px;color:#a0b3c6;font-weight:500;}}
.pii-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:15px;margin:25px 0;}}
.pii-card{{background:linear-gradient(145deg,#1a2332,#212b40);padding:18px;border-radius:15px;border-left:5px solid #00d4aa;transition:all 0.3s ease;box-shadow:0 6px 25px rgba(0,0,0,0.5);position:relative;overflow:hidden;}}
.pii-card:hover{{transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,212,170,0.3);border-left-color:#ff6b6b;}}
.pii-type{{font-weight:900;color:#00d4aa;font-size:11px;margin-bottom:8px;text-transform:uppercase;letter-spacing:1.2px;display:flex;align-items:center;}}
.pii-value{{font-family:monospace;background:#0a0e17;padding:12px;border-radius:8px;font-size:10px;color:#f8f9fa !important;border:1px solid #2d4059;font-weight:600;word-break:break-all;line-height:1.45;max-height:80px;overflow-y:auto;white-space:pre-wrap;}}
.link-btn{{display:inline-block;background:linear-gradient(45deg,#00d4aa,#0099cc);color:#000;font-weight:700;font-size:9px;padding:6px 12px;margin-top:8px;border-radius:20px;text-decoration:none;transition:all 0.3s;text-transform:uppercase;letter-spacing:0.5px;box-shadow:0 4px 15px rgba(0,212,170,0.4);}}
.link-btn:hover{{background:linear-gradient(45deg,#ff6b6b,#ff8e8e);transform:scale(1.05);box-shadow:0 6px 25px rgba(255,107,107,0.5);color:#fff !important;}}
.source-bar{{font-size:9px;color:#64748b;margin-top:10px;display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-top:1px solid #1a2332;}}
.company-section{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:30px;border-radius:20px;margin:30px 0;box-shadow:0 15px 50px rgba(102,126,234,0.4);border:1px solid rgba(255,255,255,0.1);}}
.gov-section{{background:linear-gradient(135deg,#ff6b6b,#ee5a52);padding:30px;border-radius:20px;margin:30px 0;box-shadow:0 15px 50px rgba(255,107,107,0.4);}}
.dark-section{{background:linear-gradient(135deg,#2c3e50,#34495e);padding:30px;border-radius:20px;margin:30px 0;box-shadow:0 15px 50px rgba(44,62,80,0.6);}}
.footer{{text-align:center;font-size:9px;color:#64748b;margin-top:50px;padding-top:30px;border-top:3px solid #1a2332;padding-bottom:20px;}}
@media print{{.link-btn{{color:#00d4aa !important;background:none !important;box-shadow:none !important;transform:none !important;}}body{{font-size:8px;}}.pii-grid{{grid-template-columns:repeat(6,1fr);gap:10px;}}.pii-value{{color:#000 !important;}}}}
</style>
</head>
<body>
<h1>🌐 {self.target} - GLOBAL OSINT DOSSIER v85.8</h1>

<div class="stats-grid">
<div class="stat-card"><div class="stat-number">{len(self.results)}</div><div class="stat-label">TOTAL RECORDS</div></div>
<div class="stat-card"><div class="stat-number">{len(set([r['source'] for r in self.results]))}</div><div class="stat-label">SOURCES HIT</div></div>
<div class="stat-card"><div class="stat-number">{self.company_intel.get('company', 'Scanning...')}</div><div class="stat-label">COMPANY</div></div>
<div class="stat-card"><div class="stat-number">{datetime.now().strftime('%H:%M:%S')}</div><div class="stat-label">SCAN COMPLETE</div></div>
</div>'''

        if self.company_intel.get('company'):
            html += f'''<div class="company-section">
<h2 style="color:#fff;margin:0 0 20px 0;font-size:16px;">🏢 TARGET COMPANY PROFILE</h2>
<div class="pii-grid" style="grid-template-columns:1fr;">
<div class="pii-card" style="border-left-color:#ff6b6b;">
<div class="pii-type">🏢 COMPANY IDENTIFIED</div>
<div class="pii-value">{self.company_intel['company']}</div>
</div>
</div></div>'''

        html += f'<h2 style="color:#ff6b6b;">🆔 ALL INTELLIGENCE ({len(self.results)} RECORDS FOUND)</h2><div class="pii-grid">'

        for result in self.results:
            pii_items = []
            if isinstance(result['data'], dict):
                for pii_type, pii_value in result['data'].items():
                    link = result.get('link', '#')
                    pii_items.append(f'''
<div class="pii-card">
<div class="pii-type">{pii_type}</div>
<div class="pii-value">{pii_value}</div>
<a href="{link}" target="_blank" class="link-btn">🔗 OPEN SOURCE</a>
<div class="source-bar">
<span>📡 {result["source"]}</span>
<span>⚙️ {result["engine"]}</span>
</div>
</div>''')
            else:
                link = result.get('link', '#')
                pii_items.append(f'''
<div class="pii-card">
<div class="pii-type">{result["category"]}</div>
<div class="pii-value">{result["data"]}</div>
<a href="{link}" target="_blank" class="link-btn">🔗 OPEN SOURCE</a>
<div class="source-bar">
<span>📡 {result["source"]}</span>
<span>⚙️ {result["engine"]}</span>
</div>
</div>''')
            
            html += "".join(pii_items)

        html += f'''</div>
<div class="footer">
<strong>KhalidHusain786 v85.8</strong> | {len(self.results)} Records | AADHAAR•VOTER•PAN•GLOBAL | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC<br>
<i>🔗 CLICKABLE LINKS • PASSWORDS VISIBLE • FULL PII EXTRACTION • GOVERNMENT + DARK WEB</i>
</div>
</body>
</html>'''
        
        try:
            from weasyprint import HTML
            HTML(string=html).write_pdf(
                self.target_pdf,
                stylesheets=None
            )
            print(f"{Fore.GREEN}📄 SINGLE PDF: {self.target_pdf} ({len(self.results)} records)")
        except Exception as e:
            html_file = self.target_pdf.replace('.pdf', '.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"{Fore.YELLOW}📄 HTML: {html_file} (Open in browser for clickable links)")
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        with print_lock:
            emojis = {
                "BREACH": "💥", "KALI": "⚡", "SOCIAL": "📱", "CRYPTO": "₿", 
                "USERNAME": "👤", "COMPANY": "🏢", "PASSWORD": "🔑", 
                "GOVERNMENT": "🏛️", "RESUME": "📄", "DATALAKE": "🌊", "DARKWEB": "🕸️"
            }
            emoji = emojis.get(category, "🌐")
            print(f"{Fore.GREEN}✓ [{emoji}] {Fore.CYAN}{category:12} | {Fore.YELLOW}{source:14} | {Fore.MAGENTA}{engine} | 🔗 {link[:60]}...")
            
            if isinstance(data, dict):
                for pii_type, pii_value in data.items():
                    color = Fore.RED if any(x in pii_type.upper() for x in ['PASS', 'KEY', 'HASH', 'AADHAAR', 'PAN', 'VOTER']) else Fore.WHITE
                    print(f"   {Fore.CYAN}🆔 {pii_type}: {color}{pii_value}")
            else:
                print(f"   {Fore.RED}→ {data}")
            
            print(f"{Style.RESET_ALL}")
            
            self.results.append({
                'category': category, 'data': data, 'source': source,
                'engine': engine, 'link': link if link.startswith('http') else f"https://google.com/search?q={urllib.parse.quote(self.target)}+{urllib.parse.quote(source)}",
                'network': network
            })
            
            self.update_pdf()
    
    def tor_init(self):
        try:
            if TOR_AVAILABLE:
                self.tor_session = requests.Session()
                self.tor_session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                self.cookies = {}
                print(f"{Fore.CYAN}🌀 TOR + COOKIES READY")
                return True
        except: pass
        return False
    
    def scan_url(self, url, source, engine="WEB"):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            session = self.tor_session if self.tor_session else requests
            resp = session.get(url, headers=headers, timeout=35, allow_redirects=True)
            
            if resp.cookies:
                self.cookies.update(resp.cookies.get_dict())
            
            if resp.status_code == 200:
                text = resp.text
                pii_found = self.extract_pii(text)
                
                if pii_found:
                    self.print_result(engine, pii_found, source, engine, url)
                else:
                    self.print_result(engine, {'TARGET': self.target}, source, engine, url)
                    
        except Exception as e:
            fallback_url = f"https://google.com/search?q={urllib.parse.quote(self.target)}+{urllib.parse.quote(source)}"
            self.print_result(engine, {'TARGET': self.target}, source, engine, fallback_url)
    
    def run_full_scan(self):
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 SINGLE OUTPUT: {TARGET_FOLDER}/{self.target}.pdf")
        print("="*100)
        
        self.tor_init()
        time.sleep(3)
        
        # ALL SCANS - NEW + EXISTING
        scans = [
            self.government_scan,      # NEW: Government IDs
            self.resume_pdf_scan,      # NEW: Resumes/PDFs  
            self.data_lakes_scan,      # NEW: Data Lakes
            self.darkweb_scan,         # NEW: Dark Web
            self.company_scan,
            self.password_scan,
            self.breach_scan, 
            self.username_scan, 
            self.crypto_scan,
            self.social_media_scan, 
            self.kali_tool_scan
        ]
        
        threads = [Thread(target=scan, daemon=True) for scan in scans]
        for t in threads: t.start()
        for t in threads: t.join(3000)
        
        print(f"\n{Fore.RED}✅ GLOBAL SCAN COMPLETE!")
        print(f"{Fore.GREEN}📄 SINGLE FILE: {self.target_pdf}")
        print(f"{Fore.CYAN}🔗 {len(self.results)} RECORDS - AADHAAR•VOTER•PAN•PASSWORDS•DARK WEB")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target>")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv857()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()
