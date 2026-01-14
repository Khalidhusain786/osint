#!/usr/bin/env python3
"""
KHALID HUSAIN786 ULTIMATE OSINT v85.2 - SINGLE TARGET FOLDER
FULL TOR + DARKWEB + GOVT + COMPANIES - AUTO SAVE + CLICKABLE LINKS
"""

import os
import subprocess
import sys
import requests
import re
import time
import random
import json
import urllib.parse
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

# SINGLE GLOBAL TARGET FOLDER
TARGET_FOLDER = "./Target"
os.makedirs(TARGET_FOLDER, exist_ok=True)

class KhalidHusain786OSINTv852:
    def __init__(self):
        self.target = ""
        self.results = []
        self.tor_session = None
        
    def banner(self):
        """Khalid Husain786 Banner"""
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}                  KHALID HUSAIN786                   {Fore.RED}║
{Fore.RED}║{Fore.CYAN}              ULTIMATE OSINT v85.2                {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA} SINGLE TARGET FOLDER + AUTO SAVE + LINKS      {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def auto_save_json(self):
        """Auto-save JSON continuously"""
        if self.results:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_file = f"{TARGET_FOLDER}/{self.target}_KhalidHusain786_{timestamp}.json"
            data = {
                "target": self.target,
                "timestamp": timestamp,
                "total_hits": len(self.results),
                "results": self.results
            }
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"{Fore.GREEN}💾 Auto-saved JSON: {json_file}")
    
    def tor_init(self):
        """TOR + SOCKS5 Init"""
        try:
            if not TOR_AVAILABLE:
                return False
                
            if subprocess.run(['pgrep', 'tor'], capture_output=True).returncode != 0:
                subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(10)
            
            self.tor_session = requests.Session()
            self.tor_session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            print(f"{Fore.GREEN}🌀 TOR SOCKS5 ACTIVE")
            return True
        except:
            print(f"{Fore.YELLOW}⚠️ TOR → Surface web")
            return False
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        """Display + Auto-save"""
        with print_lock:
            network_emoji = {"TOR": "🌀", "DARKWEB": "🕳️", "GOVT": "🏛️", "CORP": "🏢"}.get(network, "🌐")
            print(f"{Fore.GREEN}✓{Fore.WHITE} [{network_emoji}{network}] {Fore.CYAN}{category:12} | {Fore.YELLOW}{source:15} | {Fore.MAGENTA}{engine}")
            print(f"   {Fore.RED}→ {data}{Style.RESET_ALL}")
            if link:
                print(f"   {Fore.BLUE}🔗 {link}{Style.RESET_ALL}\n")
            
        self.results.append({
            'category': category, 'data': data, 'source': source,
            'engine': engine, 'link': link, 'network': network
        })
        
        # AUTO SAVE EVERY HIT
        self.auto_save_json()
    
    def classify_data(self, data, context=""):
        """Data classification"""
        patterns = {
            'NAME': r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b',
            'PHONE': r'[\+]?[6-9]\d{9,10}',
            'PINCODE': r'\b[1-9]\d{5}\b',
            'PAN': r'[A-Z]{5}[0-9]{4}[A-Z]',
            'VEHICLE': r'[A-Z]{2}[0-9]{1,2}[A-Z]{2}\d{4}',
            'LOCATION': r'(?:City|State|District|Area|Location)[:\s]*([A-Za-z\s,]+?)(?:\s|$|<)',
            'EMAIL': r'\b[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}\b',
            'DOMAIN': r'\b(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}\b'
        }
        
        full_text = data + ' ' + context
        for cat, pattern in patterns.items():
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            for match in matches:
                clean = re.sub(r'[^\w\s@.\-+]', '', str(match).strip())
                if len(clean) > 3:
                    return cat, clean[:50]
        return "INFO", data[:50]
    
    def scan_url(self, url, source, engine="WEB", use_tor=False):
        """Safe URL scan"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            session = self.tor_session if use_tor and self.tor_session else requests
            
            resp = session.get(url, headers=headers, timeout=25)
            if self.target.lower() in resp.text.lower():
                context = resp.text.lower()
                start = context.find(self.target.lower())
                snippet = resp.text[max(0, start-150):start+250]
                cat, clean_data = self.classify_data(self.target, snippet)
                self.print_result(cat, clean_data, source, engine, url, "TOR" if use_tor else "🌐")
        except:
            pass
    
    def darkweb_scan(self):
        """DARKWEB + TOR"""
        print(f"{Fore.RED}🕳️  DARKWEB + TOR ONIONS")
        onions = [
            ("Ahmia", "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"),
            ("Torch", "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion"),
            ("OnionLand", "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2yykyd.onion")
        ]
        
        def scan_onion(name, url):
            self.scan_url(f"{url}/?q={urllib.parse.quote(self.target)}", name, "DARKWEB", True)
        
        threads = [Thread(target=scan_onion, args=(name, url), daemon=True) for name, url in onions]
        for t in threads: t.start()
        for t in threads: t.join(45)
    
    def government_scan(self):
        """Government Databases"""
        print(f"{Fore.RED}🏛️  GOVERNMENT DATABASES")
        govt = [
            ("IncomeTax", f"https://incometaxindia.gov.in/search-result?search={urllib.parse.quote(self.target)}"),
            ("EPFO", f"https://unifiedportal-mem.epfindia.gov.in/memberinterface/#/search?q={urllib.parse.quote(self.target)}"),
            ("Passport", "https://passportindia.gov.in/AppOnlineProject/online/searchStatus"),
            ("GST", f"https://www.gst.gov.in/search?query={urllib.parse.quote(self.target)}"),
            ("Election", "https://electoralsearch.eci.gov.in/search"),
            ("MCA", f"https://www.mca.gov.in/content/mca/global/en/search-result.html?q={urllib.parse.quote(self.target)}")
        ]
        
        threads = [Thread(target=self.scan_url, args=(url, name, "GOVT"), daemon=True) for name, url in govt]
        for t in threads: t.start()
        for t in threads: t.join(35)
    
    def companies_scan(self):
        """Companies Databases"""
        print(f"{Fore.RED}🏢 COMPANIES DATABASES")
        corp = [
            ("ZaubaCorp", f"https://www.zaubacorp.com/search?q={urllib.parse.quote(self.target)}"),
            ("Tofler", f"https://www.tofler.in/search?q={urllib.parse.quote(self.target)}"),
            ("IndiaMart", f"https://dir.indiamart.com/search.mp?ss={urllib.parse.quote(self.target)}"),
            ("JustDial", f"https://www.justdial.com/search?q={urllib.parse.quote(self.target)}"),
            ("Sulekha", f"https://www.sulekha.com/search?q={urllib.parse.quote(self.target)}")
        ]
        
        threads = [Thread(target=self.scan_url, args=(url, name, "CORP"), daemon=True) for name, url in corp]
        for t in threads: t.start()
        for t in threads: t.join(35)
    
    def kali_tools(self):
        """Kali Tools"""
        print(f"{Fore.RED}⚔️  KALI LINUX TOOLS")
        tools = ['theHarvester', 'dnsenum']
        
        for tool in tools:
            try:
                if subprocess.run(['which', tool], capture_output=True).returncode == 0:
                    cmd = f"{tool} {self.target}"
                    result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=180)
                    if result.stdout and self.target in result.stdout:
                        cat, clean = self.classify_data(self.target, result.stdout)
                        self.print_result(cat, clean, tool, "KALI", f"kali://{tool}", "TOR")
            except:
                continue
    
    def generate_pdf(self):
        """PDF with CLICKABLE LINKS"""
        if not self.results:
            print(f"{Fore.YELLOW}❌ No results")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_file = f"{TARGET_FOLDER}/{self.target}_KhalidHusain786_v852_{timestamp}.pdf"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Khalid Husain786 OSINT - {self.target}</title>
    <style>
        body {{ font-family: Arial; margin: 40px; background: #1a1a1a; color: #fff; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #ff4757, #1e90ff, #00d2d3); padding: 50px; text-align: center; border-radius: 25px; margin-bottom: 50px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); }}
        h1 {{ font-size: 36px; margin: 0; text-shadow: 3px 3px 8px rgba(0,0,0,0.8); }}
        .stats {{ display: flex; gap: 35px; justify-content: center; flex-wrap: wrap; margin-top: 30px; }}
        .stat {{ background: rgba(255,255,255,0.15); padding: 20px 35px; border-radius: 20px; backdrop-filter: blur(15px); }}
        table {{ width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.08); border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        th {{ background: linear-gradient(90deg, #2f3542, #3742fa); padding: 22px; text-align: left; color: #fff; font-weight: bold; }}
        td {{ padding: 20px 22px; border-bottom: 1px solid rgba(255,255,255,0.12); }}
        a {{ color: #4ecdc4; text-decoration: none; font-weight: bold; }}
        a:hover {{ color: #ffd700; text-decoration: underline; }}
        .dark {{ background: #0f3460 !important; color: #00ff88 !important; }}
        .govt {{ background: #c44569 !important; color: #fff !important; }}
        .corp {{ background: #28a745 !important; color: #fff !important; }}
        .target {{ color: #ffd700; font-size: 28px; font-weight: bold; }}
        tr:hover {{ background: rgba(255,255,255,0.1) !important; transform: scale(1.01); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ KHALID HUSAIN786 - OSINT INTELLIGENCE v85.2</h1>
        <div class="stats">
            <div class="stat"><span class="target">{self.target}</span></div>
            <div class="stat"><strong>{len(self.results)}</strong> Intelligence Hits</div>
            <div class="stat">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
            <div class="stat">📁 ./Target/</div>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th><strong>CATEGORY</strong></th>
                <th><strong>DATA</strong></th>
                <th><strong>SOURCE</strong></th>
                <th><strong>NETWORK</strong></th>
                <th><strong>LINK</strong></th>
                <th><strong>ENGINE</strong></th>
            </tr>
        </thead>
        <tbody>
"""
        
        for result in self.results:
            link_html = f'<a href="{result["link"]}" target="_blank">{result["link"][:60]}...</a>' if result['link'] else "N/A"
            network_class = {"TOR": "dark", "DARKWEB": "dark", "GOVT": "govt", "CORP": "corp"}.get(result['network'], "")
            html += f"""
            <tr class="{network_class}">
                <td><strong>{result['category']}</strong></td>
                <td><strong>{result['data']}</strong></td>
                <td>{result['source']}</td>
                <td><strong>{result['network']}</strong></td>
                <td>{link_html}</td>
                <td>{result['engine']}</td>
            </tr>
            """
        
        html += """
        </tbody>
    </table>
</body>
</html>
        """
        
        try:
            from weasyprint import HTML
            HTML(string=html).write_pdf(pdf_file)
            print(f"{Fore.GREEN}📄 PDF with LINKS: {pdf_file}")
        except:
            html_file = pdf_file.replace('.pdf', '.html')
            with open(html_file, 'w') as f:
                f.write(html)
            print(f"{Fore.GREEN}📄 HTML with LINKS: {html_file}")
    
    def run_full_scan(self):
        """Full scan"""
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 SINGLE FOLDER: {TARGET_FOLDER}")
        print(f"{'='*85}\n")
        
        self.tor_init()
        
        scanners = [
            ("🕳️ DarkWeb", self.darkweb_scan),
            ("🏛️ Government", self.government_scan),
            ("🏢 Companies", self.companies_scan),
            ("⚔️ Kali", self.kali_tools)
        ]
        
        threads = []
        for name, func in scanners:
            print(f"{Fore.CYAN}🚀 {name} scan started...")
            t = Thread(target=func, daemon=True)
            threads.append(t)
            t.start()
        
        print(f"{Fore.CYAN}⏳ Scanning all sources (15min max)...")
        for t in threads:
            t.join(timeout=900)
        
        self.generate_pdf()
        print(f"\n{Fore.RED}🎉 KHALID HUSAIN786 v85.2 COMPLETE!")
        print(f"{Fore.GREEN}📂 ALL DATA: {TARGET_FOLDER}/")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid_osint_v852.py <target>")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv852()
    osint.target = sys.argv[1]
    osint.run_full_scan()
