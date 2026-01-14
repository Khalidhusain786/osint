#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.6 - UNLIMITED PII + PASSWORDS + COMPANY INTEL
PAN • AADHAAR • PASSWORDS • COMPANY • USERS • REGISTRATION • ALL TARGET DATA
SINGLE PDF - NO LIMITS • PERFECT SIZE
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

class KhalidHusain786OSINTv856:
    def __init__(self):
        self.target = ""
        self.results = []
        self.pdf_file = ""
        self.tor_session = None
        self.cookies = {}
        self.company_intel = {}  # NEW: Company tracking
        
    def banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}         KHALID HUSAIN786 v85.6 - UNLIMITED PII         {Fore.RED}║
{Fore.RED}║{Fore.CYAN}PASSWORDS•COMPANY•USERS•REGISTRATION•ALL TARGET DATA{Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}     SINGLE PDF • NO LIMITS • PERFECT SIZE          {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def pii_patterns(self):
        """ALL PII + PASSWORDS + COMPANY PATTERNS"""
        return {
            'PAN': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
            'AADHAAR': r'\b\d{12}\b',
            'PASSWORD': r'(?:passw[o0]rd|pwd|token|key|secret)[:\s]*["\']?([^\s"\'\n]{4,50})["\']?',
            'PASSWORD_HASH': r'\b[A-Fa-f0-9]{32,128}\b',
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
            'COMPANY': r'(?:inc|corp|ltd|llc|plc|co\.?\s?)(?:\.)?[A-Za-z\s\.\-]{2,50}',
            'LOCATION': r'\b(?:[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4}|[0-9]{4}[/-][0-9]{1,2}[/-][0-9]{1,2})\b',
            'REG_DATE': r'(?:registered|created|joined)[\s\-:]+(?:on|at)[\s\-:]+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
            'API_KEY': r'(?:api[_-]?key|token|auth[_-]?key)[:\s]*["\']?([A-Za-z0-9\-_]{20,})\b'
        }
    
    def extract_pii(self, text):
        """ENHANCED PII + COMPANY + PASSWORDS"""
        pii_data = {}
        text_lower = text.lower()
        
        patterns = self.pii_patterns()
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                # NEW: Track company details
                if pii_type == 'COMPANY' and matches:
                    self.company_intel['company'] = matches[0].strip()
                pii_data[pii_type] = matches[0][:50]  # First match
        
        # NEW: Company intel
        if self.company_intel.get('company'):
            pii_data['COMPANY'] = self.company_intel['company']
        
        if not pii_data:
            pii_data['TARGET'] = self.target[:30]
        
        return pii_data
    
    def company_scan(self):
        """NEW: COMPANY + REGISTRATION INTEL"""
        print(f"{Fore.RED}🏢 COMPANY + REGISTRATION")
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
        """NEW: PASSWORDS + TOKENS"""
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
        print(f"{Fore.RED}💥 GLOBAL BREACHES + PASSWORDS")
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
        print(f"{Fore.RED}👤 USERNAME + USERS")
        usernames = [
            ("NameCheckr", f"https://namecheckr.com/search/{urllib.parse.quote(self.target)}"),
            ("KnowEm", f"https://knowem.com/checkusernames.php?u={urllib.parse.quote(self.target)}"),
            ("Namecheap", f"https://www.namecheap.com/domains/registration/results/?domain={urllib.parse.quote(self.target)}"),
            ("Sherlock", f"python3 /usr/share/sherlock/sherlock.py {self.target}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "USERNAME"), daemon=True) for name, url in usernames if 'python' not in url]
        for t in threads: t.start()
        for t in threads: t.join(30)
    
    def kali_tool_scan(self):
        print(f"{Fore.RED}⚡ KALI + COMPANY TOOLS")
        kali_tools = [
            ("theHarvester", ["theHarvester", "-d", self.target, "-b", "all", "-l", "500"]),  # Increased limit
            ("dnsdumpster", f"https://dnsdumpster.com/?target={urllib.parse.quote(self.target)}"),
            ("Shodan", f"https://www.shodan.io/search?query={urllib.parse.quote(self.target)}"),
            ("Amass", ["amass", "enum", "-d", self.target, "-max 500"])  # Company domains
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
        print(f"{Fore.RED}₿ CRYPTO + WALLET")
        crypto = [
            ("BTC.com", f"https://btc.com/{urllib.parse.quote(self.target)}"),
            ("Blockchain", f"https://www.blockchain.com/explorer/search?search={urllib.parse.quote(self.target)}"),
            ("Etherscan", f"https://etherscan.io/search?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "CRYPTO"), daemon=True) for name, url in crypto]
        for t in threads: t.start()
        for t in threads: t.join(25)
    
    def social_media_scan(self):
        print(f"{Fore.RED}📱 SOCIAL + USERS")
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
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pdf_file = f"{TARGET_FOLDER}/{self.target}_KhalidHusain786_FULL_{timestamp}.pdf"
        
        # UNLIMITED: Show ALL results (no -40 limit)
        html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{self.target} FULL INTEL</title>
<style>body{{font-family:'Courier New',monospace;background:#0a0e17;color:#e6edf3;font-size:9px;line-height:1.2;padding:20px;max-width:100%;margin:0;}}h1{{color:#00d4aa;font-size:18px;text-align:center;margin:0 0 25px 0;font-weight:700;text-shadow:0 0 10px rgba(0,212,170,0.5);}}h2{{color:#ff6b6b;font-size:12px;border-bottom:2px solid #1a2332;padding-bottom:8px;margin:25px 0 15px 0;letter-spacing:1px;}}.stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin:20px 0;background:rgba(26,35,50,0.8);padding:20px;border-radius:10px;box-shadow:0 8px 32px rgba(0,0,0,0.3);}}.stat-card{{text-align:center;padding:15px;background:linear-gradient(135deg,#1a2332,#2d4059);border-radius:8px;border:1px solid #00d4aa;box-shadow:0 4px 15px rgba(0,212,170,0.1);}}.stat-number{{font-size:24px;font-weight:bold;color:#00d4aa;margin-bottom:5px;}}.stat-label{{font-size:10px;color:#a0b3c6;}}.pii-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin:20px 0;}}.pii-card{{background:linear-gradient(145deg,#1a2332,#212b40);padding:15px;border-radius:12px;border-left:4px solid #00d4aa;transition:all 0.3s;box-shadow:0 4px 20px rgba(0,0,0,0.4);}}.pii-card:hover{{transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,212,170,0.2);}}.pii-type{{font-weight:700;color:#00d4aa;font-size:10px;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px;}}.pii-value{{font-family:monospace;background:#0a0e17;padding:10px;border-radius:6px;font-size:10px;color:#f8f9fa;border:1px solid #1a2332;font-weight:500;word-break:break-all;line-height:1.4;}}.source-bar{{font-size:8px;color:#64748b;margin-top:8px;display:flex;justify-content:space-between;align-items:center;}}.company-section{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:25px;border-radius:15px;margin:25px 0;box-shadow:0 10px 40px rgba(102,126,234,0.3);}}.footer{{text-align:center;font-size:8px;color:#64748b;margin-top:40px;padding-top:25px;border-top:2px solid #1a2332;}}@media print{{body{{font-size:8px;}}.pii-grid{{grid-template-columns:repeat(6,1fr);gap:8px;}}h1{{font-size:16px;}}}}</style></head><body>
<h1>🎯 {self.target} - COMPLETE INTELLIGENCE DOSSIER</h1>
<div class="stats-grid">
<div class="stat-card"><div class="stat-number">{len(self.results)}</div><div class="stat-label">TOTAL RECORDS</div></div>
<div class="stat-card"><div class="stat-number">{len(set([r['source'] for r in self.results]))}</div><div class="stat-label">SOURCES</div></div>
<div class="stat-card"><div class="stat-number">{self.company_intel.get('company', 'N/A')}</div><div class="stat-label">COMPANY</div></div>
<div class="stat-card"><div class="stat-number">{datetime.now().strftime('%H:%M:%S')}</div><div class="stat-label">SCAN TIME</div></div>
</div>'''

        # COMPANY SECTION - NEW
        if self.company_intel.get('company'):
            html += f'''<div class="company-section">
<h2 style="color:#fff;margin:0 0 15px 0;">🏢 TARGET COMPANY INTELLIGENCE</h2>
<div class="pii-grid" style="grid-template-columns:1fr;">
<div class="pii-card" style="border-left-color:#ff6b6b;">
<div class="pii-type">COMPANY NAME</div>
<div class="pii-value">{self.company_intel['company']}</div>
</div>
</div></div>'''

        # ALL PII RECORDS - UNLIMITED
        html += f'<h2 style="color:#ff6b6b;">🆔 ALL PII + PASSWORDS + INTEL ({len(self.results)} RECORDS)</h2><div class="pii-grid">'
        
        for result in self.results:  # SHOW ALL - NO LIMIT!
            pii_items = []
            if isinstance(result['data'], dict):
                for pii_type, pii_value in result['data'].items():
                    pii_items.append(f'<div class="pii-card"><div class="pii-type">{pii_type}</div><div class="pii-value">{pii_value}</div><div class="source-bar"><span>{result["source"]}</span><span>{result["engine"]}</span></div></div>')
            else:
                pii_items.append(f'<div class="pii-card"><div class="pii-type">{result["category"]}</div><div class="pii-value">{result["data"]}</div><div class="source-bar"><span>{result["source"]}</span><span>{result["engine"]}</span></div></div>')
            
            html += "".join(pii_items)
        
        html += f'''</div><div class="footer">
Generated by KhalidHusain786 v85.6 | {len(self.results)} Records | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC<br>
<strong>ALL TARGET DATA INCLUDED - NO LIMITS</strong>
</div></body></html>'''
        
        try:
            from weasyprint import HTML
            HTML(string=html, base_url='').write_pdf(
                self.pdf_file, 
                stylesheets=None,
                optimize_images=True
            )
            print(f"{Fore.GREEN}📄 UNLIMITED PDF: {self.pdf_file} ({len(self.results)} records)")
        except:
            html_file = self.pdf_file.replace('.pdf', '.html')
            with open(html_file, 'w', encoding='utf-8') as f: f.write(html)
            print(f"{Fore.YELLOW}📄 HTML: {html_file}")
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        with print_lock:
            emojis = {"BREACH": "💥", "PII": "🆔", "KALI": "⚡", "SOCIAL": "📱", "CRYPTO": "₿", "USERNAME": "👤", "COMPANY": "🏢", "PASSWORD": "🔑"}
            emoji = emojis.get(category, "🌐")
            print(f"{Fore.GREEN}✓ [{emoji}] {Fore.CYAN}{category:10} | {Fore.YELLOW}{source:14} | {Fore.MAGENTA}{engine}")
            
            if isinstance(data, dict):
                for pii_type, pii_value in data.items():
                    color = Fore.RED if 'PASS' in pii_type or 'KEY' in pii_type else Fore.WHITE
                    print(f"   {Fore.CYAN}🆔 {pii_type}: {color}{pii_value}")
            else:
                print(f"   {Fore.RED}→ {data}")
            
            print(f"{Style.RESET_ALL}")
            
            self.results.append({
                'category': category, 'data': data, 'source': source,
                'engine': engine, 'link': link or '#', 'network': network
            })
            self.update_pdf()
    
    def tor_init(self):
        try:
            if TOR_AVAILABLE:
                self.tor_session = requests.Session()
                self.tor_session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
                self.cookies = {}
                print(f"{Fore.CYAN}🌀 TOR + COOKIES + COMPANY READY")
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
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
            }
            
            session = self.tor_session if self.tor_session else requests
            resp = session.get(url, headers=headers, timeout=30, allow_redirects=True)
            
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
            pass
    
    def run_full_scan(self):
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 UNLIMITED OUTPUT: {TARGET_FOLDER}")
        print("="*90)
        
        self.tor_init()
        time.sleep(3)
        
        scans = [
            self.company_scan,     # NEW: Company first
            self.password_scan,    # NEW: Passwords
            self.breach_scan, 
            self.username_scan, 
            self.crypto_scan,
            self.social_media_scan, 
            self.kali_tool_scan
        ]
        
        threads = [Thread(target=scan, daemon=True) for scan in scans]
        for t in threads: t.start()
        for t in threads: t.join(1800)  # Extended timeout
        
        print(f"\n{Fore.RED}🚀 FULL INTEL COMPLETE!")
        print(f"{Fore.GREEN}📄 UNLIMITED PDF: {self.pdf_file} ({len(self.results)} TOTAL RECORDS)")
        print(f"{Fore.CYAN}🏢 Company: {self.company_intel.get('company', 'Not found')}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target>")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv856()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()
