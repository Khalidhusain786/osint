#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.5 - ALL PII + GLOBAL BREACHES + COOKIES FIXED
PAN • AADHAAR • PHONE • VEHICLE • BTC • DOMAINS • FULL LOCATION - ALL COUNTRIES
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

class KhalidHusain786OSINTv854:
    def __init__(self):
        self.target = ""
        self.results = []
        self.pdf_file = ""
        self.tor_session = None
        self.cookies = {}  # FIXED: Cookie tracking
        
    def banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}           KHALID HUSAIN786 v85.5 - PII HUNTER            {Fore.RED}║
{Fore.RED}║{Fore.CYAN}PAN•AADHAAR•PHONE•VEHICLE•BTC•DOMAINS•LOCATION•USERSNAMES{Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}     COOKIES FIXED • GLOBAL • ALL COUNTRIES • PDF      {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def pii_patterns(self):
        """ALL PII PATTERNS - GLOBAL"""
        return {
            'PAN': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
            'AADHAAR': r'\b\d{12}\b',
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
            'LOCATION': r'\b(?:[0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{4}|[0-9]{4}[/-][0-9]{1,2}[/-][0-9]{1,2})\b'
        }
    
    def extract_pii(self, text):
        """EXTRACT ALL PII - FIXED"""
        pii_data = {}
        text_lower = text.lower()
        
        patterns = self.pii_patterns()
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                pii_data[pii_type] = matches[0][:30]  # First match only
        
        if not pii_data:
            pii_data['TARGET'] = self.target[:30]
        
        return pii_data
    
    def breach_scan(self):
        """GLOBAL BREACH DATABASES + PII"""
        print(f"{Fore.RED}💥 GLOBAL BREACHES + PII")
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
        """GLOBAL USERNAME SEARCH"""
        print(f"{Fore.RED}👤 USERNAME TRACKER")
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
        print(f"{Fore.RED}⚡ KALI + PII TOOLS")
        kali_tools = [
            ("theHarvester", ["theHarvester", "-d", self.target, "-b", "all", "-l", "200"]),
            ("dnsdumpster", f"https://dnsdumpster.com/?target={urllib.parse.quote(self.target)}"),
            ("Shodan", f"https://www.shodan.io/search?query={urllib.parse.quote(self.target)}")
        ]
        for tool_name, cmd_or_url in kali_tools:
            if isinstance(cmd_or_url, list):
                try:
                    result = subprocess.run(cmd_or_url, capture_output=True, text=True, timeout=180)
                    self.print_result("KALI", f"{self.target} | {tool_name}", "Kali", tool_name, "", "⚡")
                except: pass
            else:
                self.scan_url(cmd_or_url, tool_name, "KALI")
    
    def crypto_scan(self):
        print(f"{Fore.RED}₿ CRYPTO + BTC")
        crypto = [
            ("BTC.com", f"https://btc.com/{urllib.parse.quote(self.target)}"),
            ("Blockchain", f"https://www.blockchain.com/explorer/search?search={urllib.parse.quote(self.target)}"),
            ("Etherscan", f"https://etherscan.io/search?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "CRYPTO"), daemon=True) for name, url in crypto]
        for t in threads: t.start()
        for t in threads: t.join(25)
    
    def social_media_scan(self):
        print(f"{Fore.RED}📱 SOCIAL + USERNAMES")
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
        self.pdf_file = f"{TARGET_FOLDER}/{self.target}_KhalidHusain786_PII_{timestamp}.pdf"
        
        html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{self.target} PII</title>
<style>body{{font-family:monospace;background:#0d1117;color:#c9d1d9;font-size:11px;line-height:1.3;padding:15px;max-width:100%;}}h1{{color:#58a6ff;font-size:20px;text-align:center;margin-bottom:20px;}}h2{{color:#f0f6fc;font-size:14px;border-bottom:1px solid #30363d;padding-bottom:5px;margin:20px 0 10px 0;}}.pii-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:15px 0;}}.pii-card{{background:#161b22;padding:12px;border-radius:6px;border-left:3px solid #58a6ff;}}.pii-type{{font-weight:bold;color:#58a6ff;font-size:10px;margin-bottom:4px;}}.pii-value{{font-family:monospace;background:#0d1117;padding:6px;border-radius:3px;font-size:11px;color:#f0f6fc;}}.source{{font-size:9px;color:#8b949e;margin-top:4px;}}.footer{{text-align:center;font-size:9px;color:#8b949e;margin-top:30px;padding-top:20px;border-top:1px solid #30363d;}}@media print{{body{{font-size:10px;}}.pii-grid{{grid-template-columns:repeat(4,1fr);}}}}</style></head><body>
<h1>🔍 {self.target} - PII INTELLIGENCE REPORT</h1>
<div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:20px;">
<span><strong>{len(self.results)}</strong> PII Records</span>
<span>{datetime.now().strftime('%d/%m/%Y %H:%M')}</span>
</div>
<div class="pii-grid">'''

        for result in self.results[-40:]:
            pii_items = []
            if isinstance(result['data'], dict):
                for pii_type, pii_value in result['data'].items():
                    pii_items.append(f'<div class="pii-card"><div class="pii-type">{pii_type}</div><div class="pii-value">{pii_value}</div></div>')
            else:
                pii_items.append(f'<div class="pii-card"><div class="pii-type">{result["category"]}</div><div class="pii-value">{result["data"]}</div></div>')
            
            html += f'<div style="margin-bottom:10px;"><div style="font-size:10px;color:#8b949e;">{result["source"]} • {result["engine"]}</div>{"".join(pii_items)}</div>'
        
        html += f'''</div><div class="footer">KhalidHusain786 v85.5 | {len(self.results)} PII Records Found</div></body></html>'''
        
        try:
            from weasyprint import HTML
            HTML(string=html).write_pdf(self.pdf_file)
            print(f"{Fore.GREEN}📄 PII PDF: {self.pdf_file}")
        except:
            html_file = self.pdf_file.replace('.pdf', '.html')
            with open(html_file, 'w', encoding='utf-8') as f: f.write(html)
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        with print_lock:
            emojis = {"BREACH": "💥", "PII": "🆔", "KALI": "⚡", "SOCIAL": "📱", "CRYPTO": "₿", "USERNAME": "👤"}
            emoji = emojis.get(category, "🌐")
            print(f"{Fore.GREEN}✓ [{emoji}] {Fore.CYAN}{category:8} | {Fore.YELLOW}{source:12} | {Fore.MAGENTA}{engine}")
            
            if isinstance(data, dict):
                for pii_type, pii_value in data.items():
                    print(f"   {Fore.RED}🆔 {pii_type}: {Fore.WHITE}{pii_value}")
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
                self.cookies = {}  # FIXED: Reset cookies
                print(f"{Fore.CYAN}🌀 TOR + COOKIES READY")
                return True
        except: pass
        return False
    
    def scan_url(self, url, source, engine="WEB"):
        """ENHANCED PII SCANNER + COOKIES"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            session = self.tor_session if self.tor_session else requests
            resp = session.get(url, headers=headers, timeout=25, allow_redirects=True)
            
            # FIXED: Cookie extraction
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
        print(f"{Fore.GREEN}📁 OUTPUT: {TARGET_FOLDER}")
        print("="*80)
        
        self.tor_init()
        time.sleep(3)
        
        scans = [
            self.breach_scan, self.username_scan, self.crypto_scan,
            self.social_media_scan, self.kali_tool_scan
        ]
        
        threads = [Thread(target=scan, daemon=True) for scan in scans]
        for t in threads: t.start()
        for t in threads: t.join(1200)
        
        print(f"\n{Fore.RED}🎉 PII HUNT COMPLETE!")
        print(f"{Fore.GREEN}📄 PII PDF: {self.pdf_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target>")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv854()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()
