#!/usr/bin/env python3
"""
KHALID HUSAIN ULTIMATE OSINT v85.2 - FIXED VERSION
FULL TOR + DARKWEB + GOVT + COMPANIES - NO SELENIUM NEEDED
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
    print(f"{Fore.YELLOW}⚠️ Install socks: pip3 install PySocks")

init(autoreset=True)
print_lock = Lock()

class KhalidHusainOSINTv852:
    def __init__(self):
        self.target = ""
        self.results = []
        self.target_folder = ""
        self.tor_session = None
        
    def banner(self):
        """Khalid Husain Banner"""
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}                    KHALID HUSAIN                     {Fore.RED}║
{Fore.RED}║{Fore.CYAN}              ULTIMATE OSINT v85.2 FIXED             {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}   TOR+DARKWEB+GOVT+COMPANIES+DEEPWEB+SOCKS5   {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def tor_init(self):
        """TOR + SOCKS5 Init - Safe fallback"""
        try:
            if not TOR_AVAILABLE:
                return False
                
            # Check if tor running
            if subprocess.run(['pgrep', 'tor'], capture_output=True).returncode != 0:
                subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{Fore.YELLOW}🚀 Starting TOR...")
                time.sleep(10)
            
            # TOR Session
            self.tor_session = requests.Session()
            self.tor_session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            
            # Test TOR
            test = self.tor_session.get('http://httpbin.org/ip', timeout=15)
            print(f"{Fore.GREEN}🌀 TOR SOCKS5 ACTIVE ✅")
            return True
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ TOR unavailable: {e} - Using surface web")
            return False
    
    def create_folder(self):
        """Khalid Husain folder"""
        safe_target = re.sub(r'[^\w\-_.]', '_', self.target)[:25]
        self.target_folder = f"./Khalid_Husain_{safe_target}_OSINT_v852"
        os.makedirs(self.target_folder, exist_ok=True)
        print(f"{Fore.GREEN}📁 Folder: {self.target_folder}")
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        """Clean output"""
        with print_lock:
            print(f"{Fore.GREEN}✓{Fore.WHITE} [{network}] {Fore.CYAN}{category:10} | {Fore.YELLOW}{source} | {Fore.MAGENTA}{engine}")
            print(f"   {Fore.RED}→ {data}{Style.RESET_ALL}")
            if link:
                print(f"   {Fore.BLUE}🔗 {link}{Style.RESET_ALL}\n")
            
        self.results.append({
            'category': category, 'data': data, 'source': source,
            'engine': engine, 'link': link, 'network': network
        })
    
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
        """Safe URL scanner"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            session = self.tor_session if use_tor and self.tor_session else requests
            resp = session.get(url, headers=headers, timeout=20)
            
            if self.target.lower() in resp.text.lower():
                context = resp.text.lower()
                start = context.find(self.target.lower())
                snippet = resp.text[max(0, start-150):start+250]
                cat, clean_data = self.classify_data(self.target, snippet)
                self.print_result(cat, clean_data, source, engine, url, "TOR" if use_tor else "🌐")
        except:
            pass
    
    def darkweb_scan(self):
        """DARKWEB + TOR Onions"""
        print(f"{Fore.RED}🕳️  DARKWEB + TOR ONIONS")
        onions = [
            ("Ahmia", "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"),
            ("Torch", "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion"),
            ("OnionLand", "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2yykyd.onion"),
            ("Daniel", "http://danielas3rtn54uwmofdo3x2bsdifr47huasnmbgqzfrec5ubupvtpid.onion")
        ]
        
        def scan_onion(name, url):
            self.scan_url(f"{url}/?q={urllib.parse.quote(self.target)}", name, "DARKWEB", True)
        
        threads = []
        for name, url in onions:
            t = Thread(target=scan_onion, args=(name, url), daemon=True)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=40)
    
    def government_scan(self):
        """ALL Government Databases"""
        print(f"{Fore.RED}🏛️  GOVERNMENT DATABASES")
        govt_sites = [
            ("IncomeTax", f"https://incometaxindia.gov.in/search-result?search={urllib.parse.quote(self.target)}"),
            ("EPFO", f"https://unifiedportal-mem.epfindia.gov.in/memberinterface/#/search?q={urllib.parse.quote(self.target)}"),
            ("Passport", "https://passportindia.gov.in/AppOnlineProject/online/searchStatus"),
            ("GST", f"https://www.gst.gov.in/search?query={urllib.parse.quote(self.target)}"),
            ("Election", "https://electoralsearch.eci.gov.in/search"),
            ("MCA", f"https://www.mca.gov.in/content/mca/global/en/search-result.html?q={urllib.parse.quote(self.target)}")
        ]
        
        threads = []
        for name, url in govt_sites:
            t = Thread(target=self.scan_url, args=(url, name, "GOVT"), daemon=True)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=30)
    
    def companies_scan(self):
        """ALL Companies Databases"""
        print(f"{Fore.RED}🏢 COMPANIES + CORPORATES")
        corp_sites = [
            ("ZaubaCorp", f"https://www.zaubacorp.com/search?q={urllib.parse.quote(self.target)}"),
            ("Tofler", f"https://www.tofler.in/search?q={urllib.parse.quote(self.target)}"),
            ("IndiaMart", f"https://dir.indiamart.com/search.mp?ss={urllib.parse.quote(self.target)}"),
            ("JustDial", f"https://www.justdial.com/search?q={urllib.parse.quote(self.target)}"),
            ("Sulekha", f"https://www.sulekha.com/search?q={urllib.parse.quote(self.target)}")
        ]
        
        threads = []
        for name, url in corp_sites:
            t = Thread(target=self.scan_url, args=(url, name, "CORP"), daemon=True)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=30)
    
    def kali_tools(self):
        """Kali Linux Tools - Safe execution"""
        print(f"{Fore.RED}⚔️  KALI LINUX TOOLS")
        kali_tools = ['theHarvester', 'dnsenum', 'whois']
        
        for tool in kali_tools:
            try:
                if subprocess.run(['which', tool], capture_output=True).returncode == 0:
                    cmd = f"{tool} {self.target}"
                    result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=120)
                    if result.stdout and self.target in result.stdout:
                        cat, clean = self.classify_data(self.target, result.stdout)
                        self.print_result(cat, clean, tool, "KALI", f"kali://{tool}", "TOR")
            except:
                continue
    
    def generate_pdf(self):
        """Khalid Husain PDF Report"""
        if not self.results:
            print(f"{Fore.YELLOW}❌ No data found for {self.target}")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_file = f"{self.target_folder}/{self.target}_KhalidHusain_v852_{timestamp}.pdf"
        
        # Simple HTML PDF (no weasyprint needed if issues)
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Khalid Husain OSINT v85.2 - {self.target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #ff4757, #1e90ff); padding: 40px; text-align: center; border-radius: 20px; margin-bottom: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        h1 {{ font-size: 32px; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.7); }}
        .stats {{ display: flex; gap: 30px; justify-content: center; flex-wrap: wrap; margin-top: 25px; }}
        .stat {{ background: rgba(255,255,255,0.1); padding: 15px 25px; border-radius: 15px; }}
        table {{ width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.05); border-radius: 15px; overflow: hidden; }}
        th {{ background: #2f3542; padding: 18px; text-align: left; color: #fff; }}
        td {{ padding: 15px 18px; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .dark {{ background: #0f3460 !important; color: #00d4ff !important; }}
        .govt {{ background: #c44569 !important; color: #fff !important; }}
        .corp {{ background: #28a745 !important; color: #fff !important; }}
        .target {{ color: #ffd700; font-weight: bold; font-size: 24px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ KHALID HUSAIN - OSINT INTELLIGENCE v85.2</h1>
        <div class="stats">
            <div class="stat"><span class="target">{self.target}</span></div>
            <div class="stat"><strong>{len(self.results)}</strong> Intelligence Hits</div>
            <div class="stat">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th><strong>CATEGORY</strong></th>
                <th><strong>DATA</strong></th>
                <th><strong>SOURCE</strong></th>
                <th><strong>NETWORK</strong></th>
                <th><strong>ENGINE</strong></th>
            </tr>
        </thead>
        <tbody>
"""
        
        for result in self.results:
            network_class = {
                "TOR": "dark", "DARKWEB": "dark", 
                "GOVT": "govt", "CORP": "corp"
            }.get(result['network'], "")
            html_template += f"""
            <tr class="{network_class}">
                <td><strong>{result['category']}</strong></td>
                <td><strong>{result['data']}</strong></td>
                <td>{result['source']}</td>
                <td><strong>{result['network']}</strong></td>
                <td>{result['engine']}</td>
            </tr>
            """
        
        html_template += """
        </tbody>
    </table>
</body>
</html>
        """
        
        try:
            from weasyprint import HTML
            HTML(string=html_template).write_pdf(pdf_file)
        except ImportError:
            # Fallback: Save HTML
            with open(pdf_file.replace('.pdf', '.html'), 'w') as f:
                f.write(html_template)
            pdf_file = pdf_file.replace('.pdf', '.html')
            print(f"{Fore.YELLOW}📄 HTML Report: {pdf_file} (install weasyprint for PDF)")
            return
        
        print(f"{Fore.GREEN}📄 Khalid Husain PDF: {pdf_file}")
    
    def run_full_scan(self):
        """Execute full Khalid Husain scan"""
        self.banner()
        print(f"{Fore.WHITE}🎯 SCANNING: {Fore.YELLOW}{self.target}")
        print(f"{'='*85}\n")
        
        self.create_folder()
        self.tor_init()
        
        # Launch all scanners
        scanners = [
            ("DarkWeb", self.darkweb_scan),
            ("Government", self.government_scan),
            ("Companies", self.companies_scan),
            ("Kali", self.kali_tools)
        ]
        
        threads = []
        for name, scanner in scanners:
            print(f"{Fore.CYAN}🚀 Starting {name} scan...")
            t = Thread(target=scanner, daemon=True)
            threads.append(t)
            t.start()
        
        print(f"{Fore.CYAN}⏳ Waiting for results (max 15min)...")
        for t in threads:
            t.join(timeout=900)
        
        self.generate_pdf()
        print(f"{Fore.RED}🎉 KHALID HUSAIN v85.2 SCAN COMPLETE!")
        print(f"{Fore.GREEN}📂 Results saved: {self.target_folder}/")

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}❌ Usage: python3 khalid_osint_v852.py <target>")
        print(f"{Fore.WHITE}   Example: python3 khalid_osint_v852.py 7696408248")
        sys.exit(1)
    
    osint = KhalidHusainOSINTv852()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()

if __name__ == "__main__":
    main()
