#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.3 - SINGLE TARGET FOLDER + SINGLE PDF PER TARGET
ALL LINKS CLICKABLE IN ONE PDF - AUTO UPDATE - FULL SPECTRUM SCAN
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

# SINGLE GLOBAL TARGET FOLDER
TARGET_FOLDER = "./Target"
os.makedirs(TARGET_FOLDER, exist_ok=True)

class KhalidHusain786OSINTv853:
    def __init__(self):
        self.target = ""
        self.results = []
        self.pdf_file = ""
        self.tor_session = None
        self.kali_tools = []
        
    def banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}                  KHALID HUSAIN786 v85.3                  {Fore.RED}║
{Fore.RED}║{Fore.CYAN}      FULL SPECTRUM • SOCIAL • GOVT • PHOTOS • KALI      {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}     ALL TARGETS → ./Target/ + CLICKABLE PDF v2     {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def kali_tool_scan(self):
        """Kali Linux OSINT Tools Integration"""
        print(f"{Fore.RED}⚡ KALI LINUX TOOLS")
        kali_tools = {
            "theHarvester": f"theHarvester -d {self.target} -b all -f {TARGET_FOLDER}/{self.target}_harvest.html",
            "recon-ng": f"recon-ng -r -w {TARGET_FOLDER}/{self.target}_recon && recon-ng --module recon/domains-hosts/shodan_hostname --options SET SOURCE {self.target}",
            "maltego": f"maltego",  # Manual CE
            "spiderfoot": f"spiderfoot -s {self.target} -o {TARGET_FOLDER}/{self.target}_sf",
            "dnsrecon": f"dnsrecon -d {self.target}",
            "sublist3r": f"sublist3r -d {self.target} -o {TARGET_FOLDER}/{self.target}_subdomains.txt",
            "amass": f"amass enum -d {self.target} -o {TARGET_FOLDER}/{self.target}_amass.txt"
        }
        
        for tool, cmd in kali_tools.items():
            try:
                result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=120)
                if result.returncode == 0 or result.stdout:
                    self.print_result("KALI", f"{tool} scan complete", "Kali Linux", tool, f"file://{TARGET_FOLDER}/{self.target}_{tool.lower()}.*", "⚡")
            except: pass
    
    def git_tools_scan(self):
        """GitHub & Git Tools"""
        print(f"{Fore.RED}📂 GIT TOOLS")
        git_searches = [
            (f'"{self.target}"', "https://github.com/search?q={}+language:"),
            (f'{self.target} password', f"https://github.com/search?q={urllib.parse.quote(self.target)}+password"),
            (f'{self.target} api', f"https://github.com/search?q={urllib.parse.quote(self.target)}+api_key")
        ]
        for query, url in git_searches:
            self.scan_url(url.format(urllib.parse.quote(query)), "GitHub", "GIT")
    
    def social_media_scan(self):
        """ALL Social Media Platforms"""
        print(f"{Fore.RED}📱 SOCIAL MEDIA")
        social = {
            "Facebook": f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}",
            "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}",
            "Twitter": f"https://twitter.com/search?q={urllib.parse.quote(self.target)}&src=typed_query",
            "Instagram": f"https://www.instagram.com/explore/search/keyword/?q={urllib.parse.quote(self.target)}",
            "Telegram": f"https://t.me/s/{self.target.replace(' ', '%20')}",
            "WhatsApp": f"https://wa.me/search?query={urllib.parse.quote(self.target)}",
            "Reddit": f"https://www.reddit.com/search/?q={urllib.parse.quote(self.target)}",
            "TikTok": f"https://www.tiktok.com/search?q={urllib.parse.quote(self.target)}",
            "YouTube": f"https://www.youtube.com/results?search_query={urllib.parse.quote(self.target)}"
        }
        threads = [Thread(target=self.scan_url, args=(url, platform, "SOCIAL"), daemon=True) for platform, url in social.items()]
        for t in threads: t.start()
        for t in threads: t.join(30)
    
    def photo_scan(self):
        """Image & Photo Sources"""
        print(f"{Fore.RED}📸 PHOTOS/IMAGES")
        images = {
            "Google Images": f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(self.target)}",
            "Yandex Images": f"https://yandex.com/images/search?text={urllib.parse.quote(self.target)}",
            "TinEye": f"https://tineye.com/search/?url={urllib.parse.quote(self.target)}",
            "FaceCheck": f"https://facecheck.id/search={urllib.parse.quote(self.target)}"
        }
        threads = [Thread(target=self.scan_url, args=(url, source, "PHOTOS"), daemon=True) for source, url in images.items()]
        for t in threads: t.start()
        for t in threads: t.join(25)
    
    def update_pdf(self):
        """Enhanced PDF with ALL categories"""
        if not self.results:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pdf_file = f"{TARGET_FOLDER}/{self.target}_KhalidHusain786_FULL_SCAN_{timestamp}.pdf"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{self.target} - Khalid Husain786 FULL SPECTRUM OSINT</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Roboto', sans-serif; background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%); color: #fff; min-height: 100vh; padding: 30px; }}
        .header {{ background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57); padding: 40px; text-align: center; border-radius: 25px; margin-bottom: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); backdrop-filter: blur(20px); }}
        .header h1 {{ font-size: 42px; margin: 0 0 20px 0; text-shadow: 3px 3px 10px rgba(0,0,0,0.7); background: linear-gradient(45deg, #ffd700, #ffed4e, #ff6b6b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-top: 25px; }}
        .stat {{ background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; text-align: center; backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2); }}
        .target {{ font-size: 24px; font-weight: bold; color: #ffd700; }}
        .links-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 20px; margin-top: 30px; }}
        .link-card {{ background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02)); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.15); backdrop-filter: blur(20px); transition: all 0.3s; box-shadow: 0 8px 25px rgba(0,0,0,0.2); }}
        .link-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 35px rgba(0,0,0,0.4); }}
        .category {{ font-size: 16px; font-weight: bold; margin-bottom: 12px; padding: 10px; border-radius: 10px; display: inline-block; }}
        .social .category {{ background: linear-gradient(90deg, #e1306c, #fd1d1d); color: #fff; }}
        .kali .category {{ background: linear-gradient(90deg, #ff6b35, #f7931e); color: #fff; }}
        .photos .category {{ background: linear-gradient(90deg, #667eea, #764ba2); color: #fff; }}
        .govt .category {{ background: linear-gradient(90deg, #c44569, #dc3545); color: #fff; }}
        .dark .category {{ background: linear-gradient(90deg, #1e3c72, #2a5298); color: #00ff88; }}
        .data {{ font-size: 14px; color: #ffd700; margin-bottom: 12px; padding: 10px; background: rgba(255,215,0,0.1); border-radius: 8px; border-left: 4px solid #ffd700; }}
        .link-btn {{ display: block; width: 100%; padding: 15px; background: linear-gradient(90deg, #4ecdc4, #44bdad); color: #fff; text-decoration: none; border-radius: 12px; font-weight: bold; font-size: 14px; text-align: center; transition: all 0.3s; border: none; cursor: pointer; }}
        .link-btn:hover {{ background: linear-gradient(90deg, #45b7d1, #4ecdc4); transform: scale(1.02); box-shadow: 0 8px 20px rgba(78,205,196,0.4); }}
        .source {{ color: #a0a0a0; font-size: 12px; margin-bottom: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 {self.target} - Khalid Husain786 FULL SPECTRUM OSINT</h1>
        <div class="stats">
            <div class="stat"><div class="target">{self.target}</div><div>Target</div></div>
            <div class="stat"><strong>{len(self.results)}</strong><div>Total Hits</div></div>
            <div class="stat">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<div>Updated</div></div>
            <div class="stat">📁 ./Target/<div>Output Folder</div></div>
        </div>
    </div>
    
    <div class="links-grid">
"""
        
        # Group by category
        by_category = {}
        for result in self.results:
            cat = result['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(result)
        
        for category, hits in by_category.items():
            class_map = {
                "SOCIAL": "social", "KALI": "kali", "PHOTOS": "photos",
                "GOVT": "govt", "GIT": "kali", "DARKWEB": "dark"
            }
            css_class = class_map.get(category, "web")
            
            html += f'''
        <div class="link-card {css_class}">
            <div class="category {css_class}">{category} ({len(hits)})</div>
            <div class="data">{hits[0]["data"]}</div>
            <div class="source">{hits[0]["source"]} • {hits[0]["engine"]}</div>
            <a href="{hits[0]["link"]}" target="_blank" class="link-btn">🔗 OPEN {category} LINK</a>
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
            print(f"{Fore.GREEN}📄 FULL SPECTRUM PDF: {self.pdf_file}")
        except ImportError:
            html_file = self.pdf_file.replace('.pdf', '.html')
            with open(html_file, 'w') as f:
                f.write(html)
            print(f"{Fore.YELLOW}📄 HTML: {html_file} (pip3 install weasyprint)")
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        """Thread-safe result display + PDF update"""
        with print_lock:
            network_emoji = {"TOR": "🌀", "DARKWEB": "🕳️", "GOVT": "🏛️", "CORP": "🏢", "SOCIAL": "📱", "KALI": "⚡", "PHOTOS": "📸", "GIT": "📂"}.get(network, "🌐")
            print(f"{Fore.GREEN}✓{Fore.WHITE} [{network_emoji}{network}] {Fore.CYAN}{category:12} | {Fore.YELLOW}{source:18} | {Fore.MAGENTA}{engine}")
            print(f"   {Fore.RED}→ {data}{Style.RESET_ALL}")
            if link: print(f"   {Fore.BLUE}🔗 {link}{Style.RESET_ALL}\n")
            
        self.results.append({
            'category': category, 'data': data, 'source': source,
            'engine': engine, 'link': link, 'network': network
        })
        self.update_pdf()
    
    def tor_init(self):
        try:
            if not TOR_AVAILABLE: return False
            if subprocess.run(['pgrep', 'tor'], capture_output=True).returncode != 0:
                subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(8)
            self.tor_session = requests.Session()
            self.tor_session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
            self.print_result("TOR", "Tor network active", "Tor", "NETWORK", "", "🌀")
            return True
        except: print(f"{Fore.YELLOW}⚠️ TOR → Surface Web"); return False
    
    def classify_data(self, data, context=""):
        """Enhanced data classification"""
        patterns = {
            'NAME': r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)?)?\b',
            'PHONE': r'[\+]?[6-9]\d{9,11}',
            'EMAIL': r'\b[\w\.-]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}\b',
            'PINCODE': r'\b[1-9]\d{5}\b',
            'AADHAAR': r'\b\d{12}\b',
            'PAN': r'[A-Z]{{5}}[0-9]{{4}}[A-Z]'
        }
        full_text = (data + ' ' + context).lower()
        for cat, pattern in patterns.items():
            matches = re.findall(pattern, full_text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                clean = re.sub(r'[^\w\s@.\-+]', '', str(match).strip())
                if len(clean) > 2: return cat, clean[:60]
        return "HIT", data[:60]
    
    def scan_url(self, url, source, engine="WEB", use_tor=False):
        """Enhanced URL scanner with better matching"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            session = self.tor_session if use_tor and self.tor_session else requests
            resp = session.get(url, headers=headers, timeout=20, allow_redirects=True)
            
            if resp.status_code == 200 and self.target.lower() in resp.text.lower():
                soup = BeautifulSoup(resp.text, 'html.parser')
                context = resp.text.lower()
                start = context.find(self.target.lower())
                snippet = resp.text[max(0, start-200):start+300]
                
                # Extract title and description for better context
                title = soup.title.string if soup.title else "No title"
                desc = soup.find('meta', attrs={'name': 'description'})
                desc_text = desc['content'] if desc else ""
                
                cat, clean_data = self.classify_data(self.target, f"{title} {desc_text} {snippet}")
                self.print_result(cat, clean_data, source, engine, url, "TOR" if use_tor else "🌐")
        except Exception as e: pass
    
    def darkweb_scan(self):
        print(f"{Fore.RED}🕳️ DARKWEB SCAN")
        dark_sites = [
            ("Ahmia", "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={self.target}"),
            ("Torch", "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/?q={self.target}")
        ]
        threads = [Thread(target=self.scan_url, args=(url.format(urllib.parse.quote(self.target)), name, "DARKWEB", True), daemon=True) 
                  for name, url in dark_sites]
        for t in threads: t.start()
        for t in threads: t.join(60)
    
    def government_scan(self):
        print(f"{Fore.RED}🏛️ GOVERNMENT DATABASES")
        govt_sites = [
            ("IncomeTax", f"https://incometaxindia.gov.in/search-result?search={urllib.parse.quote(self.target)}"),
            ("EPFO", f"https://unifiedportal-mem.epfindia.gov.in/memberinterface/#/search?q={urllib.parse.quote(self.target)}"),
            ("GST Portal", f"https://www.gst.gov.in/search?query={urllib.parse.quote(self.target)}"),
            ("MCA", f"https://www.mca.gov.in/content/mca/global/en/search.html?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "GOVT"), daemon=True) for name, url in govt_sites]
        for t in threads: t.start()
        for t in threads: t.join(40)
    
    def companies_scan(self):
        print(f"{Fore.RED}🏢 COMPANIES & DIRECTORIES")
        corp_sites = [
            ("ZaubaCorp", f"https://www.zaubacorp.com/search?q={urllib.parse.quote(self.target)}"),
            ("IndiaMart", f"https://dir.indiamart.com/search.mp?ss={urllib.parse.quote(self.target)}"),
            ("JustDial", f"https://www.justdial.com/search?q={urllib.parse.quote(self.target)}"),
            "Tofler": f"https://www.tofler.in/search?q={urllib.parse.quote(self.target)}"
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "CORP"), daemon=True) for name, url in corp_sites]
        for t in threads: t.start()
        for t in threads: t.join(40)
    
    def run_full_scan(self):
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 OUTPUT: {TARGET_FOLDER}/")
        print(f"{'='*90}\n")
        
        # Initialize TOR
        self.tor_init()
        time.sleep(2)
        
        # ALL SCANS in parallel
        all_scans = [
            self.social_media_scan,
            self.photo_scan,
            self.darkweb_scan, 
            self.government_scan,
            self.companies_scan,
            self.git_tools_scan,
            self.kali_tool_scan
        ]
        
        threads = [Thread(target=scan, daemon=True) for scan in all_scans]
        for t in threads: t.start()
        for t in threads: t.join(1200)  # 20 minutes max per scan
        
        print(f"\n{Fore.RED}🎉 KHALID HUSAIN786 v85.3 FULL SPECTRUM COMPLETE!")
        print(f"{Fore.GREEN}📄 MASTER PDF: {self.pdf_file}")
        print(f"{Fore.CYAN}✨ {len(self.results)} TOTAL HITS ACROSS ALL SOURCES")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid_osint_v853.py <target_name>")
        print(f"{Fore.YELLOW}Example: python3 khalid_osint_v853.py 'John Doe'")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv853()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()
