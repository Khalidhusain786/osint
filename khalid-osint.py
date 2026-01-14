#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.2 - SINGLE TARGET FOLDER + SINGLE PDF PER TARGET
ALL LINKS CLICKABLE IN ONE PDF - AUTO UPDATE
"""

import os
import subprocess
import sys
import requests
import re
import time
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
        self.pdf_file = ""
        self.tor_session = None
        
    def banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}                  KHALID HUSAIN786                   {Fore.RED}║
{Fore.RED}║{Fore.CYAN}           SINGLE PDF PER TARGET - LINKS           {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}     ALL TARGETS → ./Target/ + CLICKABLE PDF    {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def update_pdf(self):
        """Update SINGLE PDF for this target with ALL clickable links"""
        if not self.results:
            return
        
        # SINGLE PDF PER TARGET - UPDATE EVERYTIME
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pdf_file = f"{TARGET_FOLDER}/{self.target}_KhalidHusain786_ALL_LINKS_{timestamp}.pdf"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{self.target} - Khalid Husain786 OSINT Links</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Roboto', sans-serif; 
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%); 
            color: #fff; 
            min-height: 100vh; 
            padding: 30px;
        }}
        .header {{ 
            background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4); 
            padding: 40px; 
            text-align: center; 
            border-radius: 25px; 
            margin-bottom: 40px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            backdrop-filter: blur(20px);
        }}
        .header h1 {{ 
            font-size: 42px; 
            margin: 0 0 20px 0; 
            text-shadow: 3px 3px 10px rgba(0,0,0,0.7); 
            background: linear-gradient(45deg, #ffd700, #ffed4e); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
        }}
        .stats {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 25px; 
            margin-top: 25px; 
        }}
        .stat {{ 
            background: rgba(255,255,255,0.1); 
            padding: 25px; 
            border-radius: 20px; 
            text-align: center; 
            backdrop-filter: blur(15px); 
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s;
        }}
        .stat:hover {{ transform: translateY(-5px); }}
        .target {{ font-size: 28px; font-weight: bold; color: #ffd700; }}
        .links-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr)); 
            gap: 25px; 
            margin-top: 40px; 
        }}
        .link-card {{ 
            background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02)); 
            border-radius: 20px; 
            padding: 30px; 
            border: 1px solid rgba(255,255,255,0.15); 
            backdrop-filter: blur(20px); 
            transition: all 0.3s; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        .link-card:hover {{ 
            transform: translateY(-8px); 
            box-shadow: 0 20px 40px rgba(0,0,0,0.4); 
            border-color: #4ecdc4;
        }}
        .category {{ 
            font-size: 18px; 
            font-weight: bold; 
            margin-bottom: 15px; 
            padding: 12px; 
            border-radius: 12px; 
            display: inline-block;
        }}
        .dark .category {{ background: linear-gradient(90deg, #1e3c72, #2a5298); color: #00ff88; }}
        .govt .category {{ background: linear-gradient(90deg, #c44569, #dc3545); color: #fff; }}
        .corp .category {{ background: linear-gradient(90deg, #28a745, #20c997); color: #fff; }}
        .web .category {{ background: linear-gradient(90deg, #667eea, #764ba2); color: #fff; }}
        .data {{ 
            font-size: 16px; 
            color: #ffd700; 
            margin-bottom: 15px; 
            padding: 12px; 
            background: rgba(255,215,0,0.1); 
            border-radius: 10px; 
            border-left: 4px solid #ffd700;
        }}
        .link-btn {{ 
            display: block; 
            width: 100%; 
            padding: 18px; 
            background: linear-gradient(90deg, #4ecdc4, #44bdad); 
            color: #fff; 
            text-decoration: none; 
            border-radius: 15px; 
            font-weight: bold; 
            font-size: 16px; 
            text-align: center; 
            transition: all 0.3s; 
            border: none; 
            cursor: pointer;
        }}
        .link-btn:hover {{ 
            background: linear-gradient(90deg, #45b7d1, #4ecdc4); 
            transform: scale(1.02); 
            box-shadow: 0 10px 25px rgba(78,205,196,0.4);
        }}
        .source {{ color: #a0a0a0; font-size: 14px; margin-bottom: 10px; }}
        .network {{ 
            float: right; 
            padding: 6px 15px; 
            border-radius: 20px; 
            font-size: 12px; 
            font-weight: bold; 
            text-transform: uppercase;
        }}
        .dark .network {{ background: rgba(0,255,136,0.2); color: #00ff88; }}
        .govt .network {{ background: rgba(255,107,107,0.3); color: #ff6b6b; }}
        .corp .network {{ background: rgba(40,167,69,0.3); color: #28a745; }}
        .web .network {{ background: rgba(102,126,234,0.3); color: #667eea; }}
        @media (max-width: 768px) {{ 
            .links-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 32px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 {self.target} - Khalid Husain786 OSINT Intelligence</h1>
        <div class="stats">
            <div class="stat">
                <div class="target">{self.target}</div>
                <div>Total Links Found</div>
            </div>
            <div class="stat">
                <strong>{len(self.results)}</strong>
                <div>Active Intelligence Hits</div>
            </div>
            <div class="stat">
                {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                <div>Last Updated</div>
            </div>
            <div class="stat">
                📁 ./Target/
                <div>All Targets Folder</div>
            </div>
        </div>
    </div>
    
    <div class="links-grid">
"""
        
        # Group by category for better display
        by_category = {}
        for result in self.results:
            cat = result['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(result)
        
        for category, hits in by_category.items():
            network_class = "web"
            if any("TOR" in h['network'] or "DARKWEB" in h['network'] for h in hits):
                network_class = "dark"
            elif any("GOVT" in h['network'] for h in hits):
                network_class = "govt"
            elif any("CORP" in h['network'] for h in hits):
                network_class = "corp"
            
            html += f'''
        <div class="link-card {network_class}">
            <div class="category {network_class}">{category}</div>
            <span class="network {network_class}">{hits[0]["network"]}</span>
            <div class="data">{hits[0]["data"]}</div>
            <div class="source">{hits[0]["source"]} • {hits[0]["engine"]}</div>
            <a href="{hits[0]["link"]}" target="_blank" class="link-btn">🔗 OPEN LINK</a>
        </div>
            '''
        
        html += """
    </div>
</body>
</html>
        """
        
        try:
            from weasyprint import HTML
            HTML(string=html).write_pdf(self.pdf_file)
            print(f"{Fore.GREEN}📄 SINGLE PDF UPDATED: {self.pdf_file}")
            print(f"{Fore.GREEN}✨ ALL {len(self.results)} LINKS - CLICKABLE!")
        except ImportError:
            html_file = self.pdf_file.replace('.pdf', '.html')
            with open(html_file, 'w') as f:
                f.write(html)
            print(f"{Fore.YELLOW}📄 HTML Links: {html_file} (pip3 install weasyprint)")
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        """Display + Update PDF"""
        with print_lock:
            network_emoji = {"TOR": "🌀", "DARKWEB": "🕳️", "GOVT": "🏛️", "CORP": "🏢"}.get(network, "🌐")
            print(f"{Fore.GREEN}✓{Fore.WHITE} [{network_emoji}{network}] {Fore.CYAN}{category:12} | {Fore.YELLOW}{source:15} | {Fore.MAGENTA}{engine}")
            print(f"   {Fore.RED}→ {data}{Style.RESET_ALL}")
            print(f"   {Fore.BLUE}🔗 {link}{Style.RESET_ALL}\n")
            
        self.results.append({
            'category': category, 'data': data, 'source': source,
            'engine': engine, 'link': link, 'network': network
        })
        
        # UPDATE PDF IMMEDIATELY
        self.update_pdf()
    
    def tor_init(self):
        try:
            if not TOR_AVAILABLE: return False
            if subprocess.run(['pgrep', 'tor'], capture_output=True).returncode != 0:
                subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(10)
            self.tor_session = requests.Session()
            self.tor_session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
            print(f"{Fore.GREEN}🌀 TOR ACTIVE")
            return True
        except: print(f"{Fore.YELLOW}⚠️ TOR → Surface"); return False
    
    def classify_data(self, data, context=""):
        patterns = {
            'NAME': r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b',
            'PHONE': r'[\+]?[6-9]\d{9,10}',
            'PINCODE': r'\b[1-9]\d{5}\b',
            'PAN': r'[A-Z]{5}[0-9]{4}[A-Z]',
            'EMAIL': r'\b[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}\b'
        }
        full_text = data + ' ' + context
        for cat, pattern in patterns.items():
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            for match in matches:
                clean = re.sub(r'[^\w\s@.\-+]', '', str(match).strip())
                if len(clean) > 3: return cat, clean[:50]
        return "INFO", data[:50]
    
    def scan_url(self, url, source, engine="WEB", use_tor=False):
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
        except: pass
    
    def darkweb_scan(self):
        print(f"{Fore.RED}🕳️ DARKWEB")
        onions = [
            ("Ahmia", "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"),
            ("Torch", "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion")
        ]
        threads = [Thread(target=lambda n,u: self.scan_url(f"{u}/?q={urllib.parse.quote(self.target)}", n, "DARKWEB", True), args=(name, url), daemon=True) for name, url in onions]
        for t in threads: t.start()
        for t in threads: t.join(45)
    
    def government_scan(self):
        print(f"{Fore.RED}🏛️ GOVERNMENT")
        govt = [
            ("IncomeTax", f"https://incometaxindia.gov.in/search-result?search={urllib.parse.quote(self.target)}"),
            ("EPFO", f"https://unifiedportal-mem.epfindia.gov.in/memberinterface/#/search?q={urllib.parse.quote(self.target)}"),
            ("GST", f"https://www.gst.gov.in/search?query={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "GOVT"), daemon=True) for name, url in govt]
        for t in threads: t.start()
        for t in threads: t.join(35)
    
    def companies_scan(self):
        print(f"{Fore.RED}🏢 COMPANIES")
        corp = [
            ("ZaubaCorp", f"https://www.zaubacorp.com/search?q={urllib.parse.quote(self.target)}"),
            ("IndiaMart", f"https://dir.indiamart.com/search.mp?ss={urllib.parse.quote(self.target)}"),
            ("JustDial", f"https://www.justdial.com/search?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "CORP"), daemon=True) for name, url in corp]
        for t in threads: t.start()
        for t in threads: t.join(35)
    
    def run_full_scan(self):
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 SINGLE FOLDER: {TARGET_FOLDER}")
        print(f"{'='*85}\n")
        
        self.tor_init()
        
        scanners = [
            self.darkweb_scan, self.government_scan, 
            self.companies_scan
        ]
        
        threads = [Thread(target=scan, daemon=True) for scan in scanners]
        for t in threads: t.start()
        for t in threads: t.join(900)
        
        print(f"\n{Fore.RED}🎉 KHALID HUSAIN786 COMPLETE!")
        print(f"{Fore.GREEN}📄 PDF: {self.pdf_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid_osint_v852.py <target>")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv852()
    osint.target = sys.argv[1]
    osint.run_full_scan()
