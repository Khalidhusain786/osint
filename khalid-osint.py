#!/usr/bin/env python3
"""
KHALID HUSAIN ULTIMATE OSINT v85.2
FULL TOR + DARKWEB + DEEPWEB + GOVT + COMPANIES + SOCKS5
(Authorized Pentest - All permissions granted)
"""

import os, subprocess, sys, requests, re, time, random, json, shlex, webbrowser
import socks
import socket
from colorama import Fore, Style, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
import markdown
from weasyprint import HTML
import urllib.parse
from datetime import datetime
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

init(autoreset=True)
print_lock = Lock()

class KhalidHusainOSINTv852:
    def __init__(self):
        self.target = ""
        self.results = []
        self.target_folder = ""
        self.tor_session = None
        
    def khalid_banner(self):
        """Khalid Husain Banner"""
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}                    KHALID HUSAIN                     {Fore.RED}║
{Fore.RED}║{Fore.CYAN}              ULTIMATE OSINT v85.2                {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}   TOR+DARKWEB+GOVT+COMPANIES+SOCKS5+DEEPWEB    {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def tor_setup(self):
        """TOR + SOCKS5 Setup"""
        try:
            # Start TOR
            subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(8)
            
            # TOR Session
            self.tor_session = requests.session()
            self.tor_session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            print(f"{Fore.GREEN}🌀 TOR + SOCKS5 ACTIVE")
            return True
        except:
            print(f"{Fore.YELLOW}⚠️ TOR fallback to surface web")
            return False
    
    def target_folder(self):
        """Khalid Husain target folder"""
        safe_target = re.sub(r'[^\w\-_.]', '_', self.target)[:25]
        self.target_folder = f"./Khalid_Husain_{safe_target}_OSINT_v852"
        os.makedirs(self.target_folder, exist_ok=True)
    
    def print_hit(self, category, data, source, engine, link="", network="Surface"):
        """Clean hit output"""
        network_emoji = {"TOR": "🌀", "DARKWEB": "🕳️", "GOVT": "🏛️", "CORP": "🏢"}.get(network, "🌐")
        with print_lock:
            print(f"{Fore.GREEN}✓{Fore.WHITE} [{network_emoji}{network}] {Fore.CYAN}{category:10} | {Fore.YELLOW}{source} | {Fore.MAGENTA}{engine}")
            print(f"   {Fore.RED}→ {data}{Style.RESET_ALL}")
            if link: print(f"   {Fore.BLUE}🔗 {link}{Style.RESET_ALL}\n")
            
        self.results.append({
            'category': category, 'data': data, 'source': source,
            'engine': engine, 'link': link, 'network': network
        })
    
    def categorize(self, data, context=""):
        """Enhanced categorization"""
        patterns = {
            'NAME': r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)+',
            'PHONE': r'[\+]?[6-9]\d{{9,10}}',
            'PINCODE': r'\b[1-9][0-9]{{5}}\b',
            'PAN': r'[A-Z]{{5}}[0-9]{{4}}[A-Z]',
            'VEHICLE': r'[A-Z]{{2}}[0-9]{{1,2}}[A-Z]{{2}}\d{{4}}',
            'LOCATION': r'(?:City|State|District|Area)[:\s]*([A-Za-z\s,]+?)(?:\s|<|$)',
            'EMAIL': r'[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{{2,}}',
            'DOMAIN': r'\b[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.[a-z0-9][a-z0-9-]*[a-z0-9]\b'
        }
        
        for cat, pat in patterns.items():
            matches = re.findall(pat, data + ' ' + context, re.IGNORECASE)
            for match in matches:
                clean = re.sub(r'[^\w\s@.\-+]', '', str(match).strip())[:50]
                if len(clean) > 3: return cat, clean
        return "DATA", data[:50]
    
    # 🔥 DARKWEB + TOR ONION SITES
    def darkweb_scan(self):
        """FULL DARKWEB + DEEPWEB"""
        print(f"{Fore.RED}🕳️  DARKWEB + TOR ONIONS")
        onions = [
            ("Dark Search", "http://searchzzz3sh2xf.onion"),
            ("Ahmia", "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"),
            ("Torch", "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion"),
            ("OnionLand", "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2yykyd.onion"),
            ("Daniel's", "http://danielas3rtn54uwmofdo3x2bsdifr47huasnmbgqzfrec5ubupvtpid.onion")
        ]
        
        def scan_onion(onion_name, url):
            try:
                if self.tor_session:
                    r = self.tor_session.get(f"{url}/search?q={urllib.parse.quote(self.target)}", timeout=25)
                    if self.target.lower() in r.text.lower():
                        cat, clean = self.categorize(self.target, r.text)
                        self.print_hit(cat, clean, onion_name, "TOR", url, "DARKWEB")
            except: pass
        
        threads = [Thread(target=scan_onion, args=(name, url), daemon=True) 
                  for name, url in onions]
        for t in threads: t.start()
        for t in threads: t.join(30)
    
    # 🔥 GOVERNMENT DATABASES
    def govt_databases(self):
        """ALL Government Sites"""
        print(f"{Fore.RED}🏛️  GOVERNMENT DATABASES")
        govt_sites = [
            ("IncomeTax", f"https://incometaxindia.gov.in/search-result?search={urllib.parse.quote(self.target)}"),
            ("EPFO", f"https://unifiedportal-mem.epfindia.gov.in/memberinterface/#/search?q={urllib.parse.quote(self.target)}"),
            ("Passport", f"https://www.passportindia.gov.in/AppOnlineProject/welcomeLink"),
            ("Aadhaar", f"https://uidai.gov.in/my-aadhaar/get-aadhaar.html"),
            ("PFCheck", f"https://www.epfindia.gov.in/site_en/index.php"),
            ("GSTPortal", f"https://www.gst.gov.in/search?query={urllib.parse.quote(self.target)}"),
            ("MCA", f"https://www.mca.gov.in/content/mca/global/en/home.html"),
            ("Election", f"https://electoralsearch.eci.gov.in/search"),
            ("RTO", f"https://parivahan.gov.in/parivahan/")
        ]
        
        def scan_govt(source, url):
            try:
                r = requests.get(url, timeout=20)
                if self.target.lower() in r.text.lower():
                    cat, clean = self.categorize(self.target, r.text)
                    self.print_hit(cat, clean, source, "GOVT", url, "GOVT")
            except: pass
        
        threads = [Thread(target=scan_govt, args=(name, url), daemon=True) 
                  for name, url in govt_sites]
        for t in threads: t.start()
        for t in threads: t.join(25)
    
    # 🔥 COMPANIES + CORPORATE
    def companies_scan(self):
        """ALL Companies Databases"""
        print(f"{Fore.RED}🏢 COMPANIES + CORPORATES")
        corp_sites = [
            ("ZaubaCorp", f"https://www.zaubacorp.com/search?q={urllib.parse.quote(self.target)}"),
            ("Tofler", f"https://www.tofler.in/search?q={urllib.parse.quote(self.target)}"),
            ("IndiaMart", f"https://dir.indiamart.com/search.mp?ss={urllib.parse.quote(self.target)}"),
            ("JustDial", f"https://www.justdial.com/search?q={urllib.parse.quote(self.target)}"),
            ("TradeIndia", f"https://www.tradeindia.com/search.html?search={urllib.parse.quote(self.target)}"),
            ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}"),
            ("Sulekha", f"https://www.sulekha.com/search?q={urllib.parse.quote(self.target)}")
        ]
        
        def scan_corp(source, url):
            try:
                r = requests.get(url, timeout=20)
                if self.target.lower() in r.text.lower():
                    cat, clean = self.categorize(self.target, r.text)
                    self.print_hit(cat, clean, source, "CORP", url, "CORP")
            except: pass
        
        threads = [Thread(target=scan_corp, args=(name, url), daemon=True) 
                  for name, url in corp_sites]
        for t in threads: t.start()
        for t in threads: t.join(25)
    
    # 🔥 KALI TOOLS
    def kali_scan(self):
        """Kali Linux Tools"""
        print(f"{Fore.RED}⚔️  KALI LINUX TOOLS")
        tools = ['theHarvester', 'sublist3r', 'dnsrecon']
        for tool in tools:
            if os.system(f"which {tool} >/dev/null 2>&1") == 0:
                cmd = f"{tool} -d {self.target} -l 100"
                try:
                    result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=180)
                    if result.stdout:
                        cat, clean = self.categorize(self.target, result.stdout)
                        self.print_hit(cat, clean, tool, "KALI", f"kali://{tool}", "TOR")
                except: pass
    
    def khalid_pdf(self):
        """Khalid Husain PDF Report"""
        if not self.results:
            print(f"{Fore.YELLOW}❌ No hits found")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        pdf_name = f"{self.target_folder}/{self.target}_KhalidHusain_v852_{timestamp}.pdf"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Khalid Husain OSINT v85.2 - {self.target}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {{ font-family: 'Roboto', sans-serif; margin: 0; padding: 30px; background: #0a0a0a; color: #fff; }}
        .header {{ background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1); padding: 40px; text-align: center; border-radius: 20px; margin-bottom: 40px; }}
        .header h1 {{ font-size: 36px; margin: 0; text-shadow: 3px 3px 6px rgba(0,0,0,0.5); }}
        .stats {{ display: flex; gap: 25px; justify-content: center; flex-wrap: wrap; margin-top: 25px; }}
        .stat {{ background: rgba(255,255,255,0.1); padding: 20px 30px; border-radius: 15px; backdrop-filter: blur(10px); }}
        table {{ width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.05); border-radius: 15px; overflow: hidden; }}
        th {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: left; }}
        td {{ padding: 18px 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .darkweb {{ background: #1a1a2e !important; color: #00ff88 !important; }}
        .govt {{ background: #dc3545 !important; color: #fff !important; }}
        .corp {{ background: #28a745 !important; color: #fff !important; }}
        .target {{ font-size: 24px; font-weight: bold; color: #ffd700; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ KHALID HUSAIN - OSINT v85.2</h1>
        <div class="stats">
            <div class="stat"><span class="target">{self.target}</span></div>
            <div class="stat"><strong>{len(self.results)}</strong> Total Hits</div>
            <div class="stat">{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
        </div>
    </div>
    
    <table>
        <tr><th>CATEGORY</th><th>DATA</th><th>SOURCE</th><th>NETWORK</th><th>ENGINE</th></tr>
"""
        
        for r in self.results:
            network_class = {"DARKWEB": "darkweb", "GOVT": "govt", "CORP": "corp"}.get(r['network'], "")
            html_content += f"""
        <tr class="{network_class}">
            <td><strong>{r['category']}</strong></td>
            <td><strong>{r['data']}</strong></td>
            <td>{r['source']}</td>
            <td><strong>{r['network']}</strong></td>
            <td>{r['engine']}</td>
        </tr>
            """
        
        html_content += "</table></body></html>"
        
        HTML(string=html_content).write_pdf(pdf_name)
        print(f"{Fore.GREEN}📄 Khalid Husain PDF: {pdf_name}")
    
    def ultimate_scan(self):
        """Khalid Husain Ultimate Scan"""
        self.khalid_banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}\n{'='*85}")
        
        self.target_folder()
        self.tor_setup()
        
        # ALL SCANS PARALLEL
        scans = [
            self.darkweb_scan,
            self.govt_databases, 
            self.companies_scan,
            self.kali_scan
        ]
        
        threads = [Thread(target=scan, daemon=True) for scan in scans]
        for t in threads: t.start()
        for t in threads: t.join(timeout=900)  # 15 min max
        
        self.khalid_pdf()
        print(f"{Fore.RED}🎉 KHALID HUSAIN v85.2 COMPLETE!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}python3 khalid_osint_v852.py <target>")
        sys.exit(1)
    
    osint = KhalidHusainOSINTv852()
    osint.target = sys.argv[1]
    osint.ultimate_scan()
