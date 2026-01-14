#!/usr/bin/env python3
"""
Ultimate OSINT v85.2 - FULL TOR + DARKWEB + DEEPWEB + GOVT + COMPANIES
Khalid Husain - ALL TOR ONION + SOCKS + HIDDEN DATA COLLECTOR
"""

import os, subprocess, sys, requests, re, time, random, json, shlex, webbrowser, socks
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
import stem.control

init(autoreset=True)
print_lock = Lock()

class UltimateOSINTv852:
    def __init__(self):
        self.target = ""
        self.results = []
        self.target_folder = ""
        self.tor_session = None
        self.tor_socks_session = None
        
    def khalid_husain_banner(self):
        """Khalid Husain Banner"""
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}           ULTIMATE OSINT v85.2 - KHALID HUSAIN          {Fore.RED}║
{Fore.RED}║{Fore.CYAN}    FULL TOR + DARKWEB + DEEPWEB + GOVT + COMPANIES    {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def start_tor(self):
        """Start TOR + SOCKS5"""
        try:
            # Start TOR if not running
            if subprocess.run(['pgrep', 'tor'], capture_output=True).returncode != 0:
                subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(10)
            
            # TOR Session
            self.tor_session = requests.session()
            self.tor_session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            
            # SOCKS Session
            self.tor_socks_session = requests.session()
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            
            print(f"{Fore.GREEN}✅ TOR + SOCKS5 Active")
            return True
        except:
            print(f"{Fore.YELLOW}⚠️ TOR failed - using surface web")
            return False
    
    def create_target_folder(self):
        """Create Khalid Husain target folder"""
        safe_target = re.sub(r'[^\w\-_.]', '_', self.target)[:30]
        self.target_folder = f"./Khalid_Husain_{safe_target}_OSINT"
        os.makedirs(self.target_folder, exist_ok=True)
        print(f"{Fore.GREEN}📁 Khalid Husain folder: {self.target_folder}")
    
    def print_clean_hit(self, category, data, source, engine, link="", network="Surface"):
        """Enhanced output with network type"""
        with print_lock:
            network_tag = f"({network})"
            print(f"{Fore.RED}✓{Fore.WHITE} {category:12} | {Fore.CYAN}{source} {network_tag:10} | {Fore.MAGENTA}{engine}{Style.RESET_ALL}")
            print(f"   {Fore.YELLOW}{data}{Style.RESET_ALL}")
            if link:
                print(f"   {Fore.BLUE}🔗 {link} {Style.RESET_ALL}")
            print()
        
        self.results.append({
            "category": category, "data": data, "source": source,
            "engine": engine, "link": link, "network": network
        })
    
    def categorize_data(self, data, html_context=""):
        """Enhanced categorization"""
        patterns = {
            'NAME': r'(?:Name|Full Name|Khalid Husain)[:\s]*([A-Za-z\s]+?)(?:\s|$|<)',
            'PHONE': r'[\+]?[6-9]\d{9,10}',
            'PINCODE': r'\b[1-9][0-9]{5}\b',
            'PAN': r'[A-Z]{5}[0-9]{4}[A-Z]',
            'VEHICLE': r'[A-Z]{2}[0-9]{1,2}[A-Z]{2}\d{4}',
            'LOCATION': r'(?:Location|City|Address|Punjab|Delhi|Mumbai)[:\s]*([A-Za-z\s,]+?)(?:\s|$|<)',
            'USERNAME': r'(?:@|handle|username)[:\s]*([a-zA-Z0-9_]+)',
            'DOMAIN': r'\b(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9][a-z0-9-]*[a-z0-9]\b',
            'IP': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'BTC': r'1[1-9A-HJ-NP-Za-km-z]{32,33}|3[1-9A-HJ-NP-Za-km-z]{32,33}|bc1[a-z0-9]{39,59}',
            'EMAIL': r'[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}'
        }
        
        for category, pattern in patterns.items():
            matches = re.findall(pattern, data + ' ' + html_context, re.IGNORECASE)
            for match in matches:
                clean_match = re.sub(r'[^\w\s@.\-+]', '', match.strip())[:50]
                if len(clean_match) > 3:
                    return category, clean_match
        return "DATA", data[:50]
    
    def scan_tor_onion(self, onion_url, source, engine="TOR"):
        """Scan TOR onion sites"""
        try:
            if self.tor_session:
                res = self.tor_session.get(onion_url, timeout=20)
                html = res.text
                soup = BeautifulSoup(html, 'html.parser')
                text_content = soup.get_text()
                
                if self.target.lower() in text_content.lower():
                    context_start = text_content.lower().find(self.target.lower())
                    context_snippet = text_content[max(0, context_start-100):context_start+200]
                    category, clean_data = self.categorize_data(self.target, context_snippet)
                    self.print_clean_hit(category, clean_data, source, engine, onion_url, "TOR")
        except:
            pass
    
    def scan_govt_sites(self):
        """ALL Government websites"""
        print(f"{Fore.RED}[🏛️ GOVERNMENT DATABASES]")
        govt_sites = [
            ("IncomeTax", f"https://incometaxindia.gov.in/search-result?search={urllib.parse.quote(self.target)}"),
            ("EPFO", f"https://unifiedportal-mem.epfindia.gov.in/memberinterface/#/search"),
            ("Passport", f"https://passportindia.gov.in/AppOnlineProject/online/searchStatus"),
            ("Aadhaar", f"https://uidai.gov.in/my-aadhaar/get-aadhaar.html"),
            ("PF", f"https://www.epfindia.gov.in/site_en/index.php"),
            ("GST", f"https://www.gst.gov.in/search"),
            ("MCA", f"https://www.mca.gov.in/content/mca/global/en/home.html"),
            ("RTO", f"https://parivahan.gov.in/parivahan/"),
            ("Election", f"https://electoralsearch.eci.gov.in/search"),
        ]
        
        threads = []
        for source, url in govt_sites:
            t = Thread(target=self.scan_url_enhanced, args=(url, source, "GOVT"), daemon=True)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=20)
    
    def scan_companies_databases(self):
        """ALL Companies + Corporate databases"""
        print(f"{Fore.RED}[🏢 COMPANIES + CORPORATE]")
        company_sites = [
            ("Zaubacorp", f"https://www.zaubacorp.com/search?q={urllib.parse.quote(self.target)}"),
            ("Tofler", f"https://www.tofler.in/search?q={urllib.parse.quote(self.target)}"),
            ("IndiaMart", f"https://dir.indiamart.com/search.mp?ss={urllib.parse.quote(self.target)}"),
            ("JustDial", f"https://www.justdial.com/search?q={urllib.parse.quote(self.target)}"),
            ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}"),
            ("Crunchbase", f"https://www.crunchbase.com/textsearch?q={urllib.parse.quote(self.target)}"),
        ]
        
        threads = []
        for source, url in company_sites:
            t = Thread(target=self.scan_url_enhanced, args=(url, source, "CORP"), daemon=True)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=20)
    
    def scan_darkweb_onions(self):
        """DARKWEB + DEEPWEB onion sites"""
        print(f"{Fore.RED}[🕳️ DARKWEB + DEEPWEB TOR]")  
        onion_sites = [
            ("DarkSearch", "http://search7tdrcvri22rieiwgi5g46qnwsesvnubqhl4juhqghso6tynuqqd.onion"),
            ("Ahmia", "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"),
            ("Torch", "http://torchdeedpnxgz26.onion"),
            ("OnionLand", "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2yykyd.onion"),
            ("DarkFail", "http://darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion"),
        ]
        
        threads = []
        for source, onion in onion_sites:
            t = Thread(target=self.scan_tor_onion, args=(onion, source, "DARKWEB"), daemon=True)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=30)
    
    def scan_url_enhanced(self, url, source, engine="WEB"):
        """Enhanced surface web scanner"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            if self.tor_session and random.choice([True, False]):
                res = self.tor_session.get(url, headers=headers, timeout=20)
            else:
                res = requests.get(url, headers=headers, timeout=15)
            
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            text_content = soup.get_text()
            
            if self.target.lower() in text_content.lower():
                context_start = text_content.lower().find(self.target.lower())
                context_snippet = text_content[max(0, context_start-100):context_start+200]
                category, clean_data = self.categorize_data(self.target, context_snippet)
                self.print_clean_hit(category, clean_data, source, engine, url, "Surface")
        except:
            pass
    
    def kali_enhanced(self):
        """Kali tools with TOR support"""
        print(f"{Fore.RED}[⚔️ KALI + TOR]")
        tools = ['nmap', 'subfinder', 'gobuster']
        for tool in tools:
            if subprocess.run(['which', tool], capture_output=True).returncode == 0:
                cmd = f"{tool} {self.target}"
                try:
                    result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=120)
                    if result.stdout:
                        category, data = self.categorize_data(self.target, result.stdout)
                        self.print_clean_hit(category, data, tool.upper(), "KALI", f"kali://{tool}", "TOR")
                except:
                    pass
    
    def generate_target_pdf(self):
        """Khalid Husain PDF - ALL NETWORKS"""
        if not self.results:
            print(f"{Fore.YELLOW}❌ No data found")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        pdf_filename = f"{self.target_folder}/{self.target}_KhalidHusain_v852_{timestamp}.pdf"
        
        pdf_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Khalid Husain OSINT v85.2 - {self.target}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial; margin: 40px; line-height: 1.6; }}
        .banner {{ background: linear-gradient(90deg, #dc3545, #007bff); color: white; padding: 30px; text-align: center; border-radius: 15px; margin-bottom: 30px; }}
        h1 {{ font-size: 28px; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .stats {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 20px; }}
        .stat {{ background: rgba(255,255,255,0.2); padding: 15px 25px; border-radius: 25px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f8f9fa; font-weight: bold; }}
        .tor {{ background: #1a1a2e !important; color: #00ff88 !important; }}
        .dark {{ background: #0f0f23 !important; color: #ff6b6b !important; }}
        .govt {{ background: #dc3545 !important; color: white !important; }}
        .category {{ font-weight: bold; text-transform: uppercase; font-size: 12px; padding: 5px 10px; border-radius: 15px; }}
    </style>
</head>
<body>
    <div class="banner">
        <h1>🛡️ KHALID HUSAIN - ULTIMATE OSINT v85.2</h1>
        <div class="stats">
            <div class="stat"><strong>{self.target}</strong></div>
            <div class="stat"><strong>{len(self.results)}</strong> Hits</div>
            <div class="stat"><strong>{datetime.now().strftime('%Y-%m-%d %H:%M')}</strong></div>
            <div class="stat tor">🕳️ TOR + DARKWEB</div>
            <div class="stat govt">🏛️ Government DBs</div>
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
            network_class = {"TOR": "tor", "DARKWEB": "dark", "GOVT": "govt"}.get(result['network'], "")
            pdf_html += f"""
            <tr>
                <td><span class="category {network_class}">{result['category']}</span></td>
                <td><strong>{result['data']}</strong></td>
                <td>{result['source']}</td>
                <td><strong>{result['network']}</strong></td>
                <td>{result['engine']}</td>
            </tr>
            """
        
        pdf_html += """
        </tbody>
    </table>
</body>
</html>
        """
        
        HTML(string=pdf_html).write_pdf(pdf_filename)
        print(f"{Fore.GREEN}📄 Khalid Husain PDF: {pdf_filename}")
    
    def ultimate_scan_v852(self):
        """Khalid Husain Ultimate Scan"""
        self.khalid_husain_banner()
        print(f"{Fore.CYAN}🎯 Target: {self.target}")
        print("=" * 80)
        
        self.create_target_folder()
        self.start_tor()
        
        # ALL SCANNERS
        threads = [
            Thread(target=self.kali_enhanced, daemon=True),
            Thread(target=self.scan_govt_sites, daemon=True),
            Thread(target=self.scan_companies_databases, daemon=True),
            Thread(target=self.scan_darkweb_onions, daemon=True),
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=600)
        
        self.generate_target_pdf()

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 osint_v852.py <target>")
        sys.exit(1)
    
    osint = UltimateOSINTv852()
    osint.target = sys.argv[1]
    osint.ultimate_scan_v852()

if __name__ == "__main__":
    main()
