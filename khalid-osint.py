#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.4 - SINGLE TARGET FOLDER + SINGLE PDF PER TARGET
ALL LINKS CLICKABLE + BREACH DATA + FULL SPECTRUM SCAN - ERROR FREE
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

class KhalidHusain786OSINTv854:
    def __init__(self):
        self.target = ""
        self.results = []
        self.pdf_file = ""
        self.tor_session = None
        
    def banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}                KHALID HUSAIN786 v85.4                 {Fore.RED}║
{Fore.RED}║{Fore.CYAN}   FULL SPECTRUM + BREACH DATA + ALL LEAKS + KALI       {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}     SINGLE PDF • CLICKABLE • ./Target/ OUTPUT      {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def breach_scan(self):
        """ALL Breach Data Sources"""
        print(f"{Fore.RED}💥 BREACH DATA & LEAKS")
        breach_sources = [
            ("HaveIBeenPwned", f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"),
            ("Dehashed", f"https://dehashed.com/search?query={urllib.parse.quote(self.target)}"),
            ("LeakCheck", f"https://leakcheck.io/api/?key=demo&q={urllib.parse.quote(self.target)}"),
            ("BreachDirectory", f"https://breachdirectory.org/search?email={urllib.parse.quote(self.target)}"),
            ("Snusbase", f"https://snusbase.com/search?q={urllib.parse.quote(self.target)}"),
            ("IntelligenceX", f"https://intelx.io/search?term={urllib.parse.quote(self.target)}&tab=emails"),
            ("Leak-Lookup", f"https://leak-lookup.com/search?query={urllib.parse.quote(self.target)}"),
            ("Firefox Monitor", f"https://monitor.firefox.com/scan/{urllib.parse.quote(self.target)}"),
            ("CyberNews", f"https://cybernews.com/personal-data-leak-check/?email={urllib.parse.quote(self.target)}"),
            ("DataBreaches", f"https://www.databreaches.net/?s={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "BREACH"), daemon=True) for name, url in breach_sources]
        for t in threads: t.start()
        for t in threads: t.join(35)
    
    def kali_tool_scan(self):
        """Kali Linux OSINT Tools - Fixed execution"""
        print(f"{Fore.RED}⚡ KALI LINUX TOOLS")
        kali_tools = [
            ("theHarvester", ["theHarvester", "-d", self.target, "-b", "google,bing,duckduckgo", "-l", "100"]),
            ("dnsrecon", ["dnsrecon", "-d", self.target]),
            ("sublist3r", ["sublist3r", "-d", self.target, "-o", f"{TARGET_FOLDER}/{self.target}_subs.txt"]),
            ("amass", ["amass", "enum", "-d", self.target, "-o", f"{TARGET_FOLDER}/{self.target}_amass.txt"])
        ]
        
        for tool_name, cmd in kali_tools:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
                if result.returncode == 0 or result.stdout.strip():
                    self.print_result("KALI", f"{tool_name} scan completed", "Kali Linux", tool_name, f"file://{TARGET_FOLDER}/{self.target}_{tool_name.lower()}.*", "⚡")
            except subprocess.TimeoutExpired:
                self.print_result("KALI", f"{tool_name} timeout (heavy scan)", "Kali Linux", tool_name, "", "⚡")
            except Exception:
                pass
    
    def git_tools_scan(self):
        """GitHub & Git Tools - Fixed syntax"""
        print(f"{Fore.RED}📂 GITHub LEAKS & REPOS")
        git_searches = [
            (f'"{self.target}"', "https://github.com/search?q={}&type=repositories"),
            (f'{self.target}+password', "https://github.com/search?q={}&type=code"),
            (f'{self.target}+api_key', "https://github.com/search?q={}&type=code"),
            (f'{self.target}+token', "https://github.com/search?q={}&type=code")
        ]
        for query, base_url in git_searches:
            url = base_url.format(urllib.parse.quote(query))
            self.scan_url(url, "GitHub", "GIT")
    
    def social_media_scan(self):
        """ALL Social Media - Fixed"""
        print(f"{Fore.RED}📱 SOCIAL MEDIA")
        social = {
            "Facebook": f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}",
            "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}",
            "Twitter": f"https://twitter.com/search?q={urllib.parse.quote(self.target)}&src=typed_query&f=live",
            "Instagram": f"https://www.instagram.com/explore/search/keyword/?q={urllib.parse.quote(self.target)}",
            "Telegram": f"https://t.me/s/{self.target.replace(' ', '%20')}",
            "Reddit": f"https://www.reddit.com/search/?q={urllib.parse.quote(self.target)}&type=link",
            "TikTok": f"https://www.tiktok.com/search?q={urllib.parse.quote(self.target)}&lang=en",
            "YouTube": f"https://www.youtube.com/results?search_query={urllib.parse.quote(self.target)}",
            "Pinterest": f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(self.target)}"
        }
        threads = []
        for platform, url in social.items():
            t = Thread(target=self.scan_url, args=(url, platform, "SOCIAL"), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(25)
    
    def photo_scan(self):
        """Image Sources - Fixed"""
        print(f"{Fore.RED}📸 PHOTOS & FACIAL RECOGNITION")
        images = {
            "Google Images": f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(self.target)}",
            "Yandex Images": f"https://yandex.com/images/search?text={urllib.parse.quote(self.target)}",
            "Bing Images": f"https://www.bing.com/images/search?q={urllib.parse.quote(self.target)}",
            "TinEye": f"https://tineye.com/search/?url={urllib.parse.quote(self.target)}",
            "PimEyes": f"https://pimeyes.com/en/search/?q={urllib.parse.quote(self.target)}",
            "FaceCheck": f"https://facecheck.id/search={urllib.parse.quote(self.target)}"
        }
        threads = []
        for source, url in images.items():
            t = Thread(target=self.scan_url, args=(url, source, "PHOTOS"), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(25)
    
    def update_pdf(self):
        """Enhanced PDF generator"""
        if not self.results:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pdf_file = f"{TARGET_FOLDER}/{self.target}_KhalidHusain786_FULL_BREACH_SCAN_{timestamp}.pdf"
        
        html = f'''<!DOCTYPE html>
<html><head><title>{self.target} - Khalid Husain786 FULL BREACH SCAN</title>
<style>@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
* {{margin:0;padding:0;box-sizing:border-box;}}body{{font-family:'Roboto',sans-serif;background:linear-gradient(135deg,#0f0f23 0%,#1a1a2e 50%,#16213e 100%);color:#fff;min-height:100vh;padding:30px;}}
.header{{background:linear-gradient(135deg,#ff6b6b,#4ecdc4,#45b7d1,#96ceb4,#feca57);padding:40px;text-align:center;border-radius:25px;margin-bottom:40px;box-shadow:0 20px 40px rgba(0,0,0,0.4);backdrop-filter:blur(20px);}}
.header h1{{font-size:42px;margin:0 0 20px 0;text-shadow:3px 3px 10px rgba(0,0,0,0.7);background:linear-gradient(45deg,#ffd700,#ffed4e,#ff6b6b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:20px;margin-top:25px;}}.stat{{background:rgba(255,255,255,0.1);padding:20px;border-radius:15px;text-align:center;backdrop-filter:blur(15px);border:1px solid rgba(255,255,255,0.2);}}
.links-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:20px;margin-top:30px;}}.link-card{{background:linear-gradient(145deg,rgba(255,255,255,0.08),rgba(255,255,255,0.02));border-radius:15px;padding:25px;border:1px solid rgba(255,255,255,0.15);backdrop-filter:blur(20px);transition:all 0.3s;box-shadow:0 8px 25px rgba(0,0,0,0.2);}}
.link-card:hover{{transform:translateY(-5px);box-shadow:0 15px 35px rgba(0,0,0,0.4);}}.category{{font-size:16px;font-weight:bold;margin-bottom:12px;padding:10px;border-radius:10px;display:inline-block;}}
.breach .category{{background:linear-gradient(90deg,#dc3545,#ff6b6b);color:#fff;}}.social .category{{background:linear-gradient(90deg,#e1306c,#fd1d1d);color:#fff;}}.kali .category{{background:linear-gradient(90deg,#ff6b35,#f7931e);color:#fff;}}.photos .category{{background:linear-gradient(90deg,#667eea,#764ba2);color:#fff;}}.govt .category{{background:linear-gradient(90deg,#c44569,#dc3545);color:#fff;}}.data{{font-size:14px;color:#ffd700;margin-bottom:12px;padding:10px;background:rgba(255,215,0,0.1);border-radius:8px;border-left:4px solid #ffd700;}}.link-btn{{display:block;width:100%;padding:15px;background:linear-gradient(90deg,#4ecdc4,#44bdad);color:#fff;text-decoration:none;border-radius:12px;font-weight:bold;font-size:14px;text-align:center;transition:all 0.3s;border:none;cursor:pointer;}}.link-btn:hover{{background:linear-gradient(90deg,#45b7d1,#4ecdc4);transform:scale(1.02);box-shadow:0 8px 20px rgba(78,205,196,0.4);}}.source{{color:#a0a0a0;font-size:12px;margin-bottom:8px;}}</style></head><body>
<div class="header"><h1>🔍 {self.target} - Khalid Husain786 FULL BREACH & LEAK SCAN</h1><div class="stats">
<div class="stat"><div class="target">{self.target}</div><div>Target</div></div><div class="stat"><strong>{len(self.results)}</strong><div>Total Hits</div></div><div class="stat">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<div>Updated</div></div><div class="stat">📁 ./Target/<div>Output</div></div></div></div><div class="links-grid">'''

        # Group results by category
        by_category = {}
        for result in self.results[-50:]:  # Last 50 for PDF size
            cat = result['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(result)
        
        for category, hits in by_category.items():
            class_map = {"BREACH": "breach", "SOCIAL": "social", "KALI": "kali", "PHOTOS": "photos", "GOVT": "govt", "GIT": "kali"}
            css_class = class_map.get(category, "web")
            html += f'''<div class="link-card {css_class}"><div class="category {css_class}">{category} ({len(hits)})</div><div class="data">{hits[0]["data"]}</div><div class="source">{hits[0]["source"]} • {hits[0]["engine"]}</div><a href="{hits[0]["link"]}" target="_blank" class="link-btn">🔗 OPEN {category}</a></div>'''
        
        html += "</div></body></html>"
        
        try:
            from weasyprint import HTML
            HTML(string=html).write_pdf(self.pdf_file)
            print(f"{Fore.GREEN}📄 BREACH PDF GENERATED: {self.pdf_file}")
        except ImportError:
            html_file = self.pdf_file.replace('.pdf', '.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"{Fore.YELLOW}📄 HTML Report: {html_file}")
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        """Thread-safe printing"""
        with print_lock:
            network_emojis = {
                "TOR": "🌀", "DARKWEB": "🕳️", "GOVT": "🏛️", "CORP": "🏢", 
                "SOCIAL": "📱", "KALI": "⚡", "PHOTOS": "📸", "GIT": "📂", "BREACH": "💥"
            }
            emoji = network_emojis.get(network, "🌐")
            print(f"{Fore.GREEN}✓{Fore.WHITE} [{emoji}{network}] {Fore.CYAN}{category:10} | {Fore.YELLOW}{source:18} | {Fore.MAGENTA}{engine}")
            print(f"   {Fore.RED}→ {data}{Style.RESET_ALL}")
            if link: print(f"   {Fore.BLUE}🔗 {link[:100]}...{Style.RESET_ALL}\n")
            
        self.results.append({
            'category': category, 'data': data[:80], 'source': source,
            'engine': engine, 'link': link, 'network': network
        })
        if len(self.results) % 5 == 0:  # Update PDF every 5 results
            self.update_pdf()
    
    def tor_init(self):
        """TOR Setup - Fixed"""
        try:
            if TOR_AVAILABLE and subprocess.run(['pgrep', 'tor'], capture_output=True).returncode != 0:
                subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(8)
            if TOR_AVAILABLE:
                self.tor_session = requests.Session()
                self.tor_session.proxies = {
                    'http': 'socks5h://127.0.0.1:9050', 
                    'https': 'socks5h://127.0.0.1:9050'
                }
                self.print_result("TOR", "Tor network initialized", "Tor", "NETWORK", "", "🌀")
                return True
        except:
            pass
        print(f"{Fore.YELLOW}⚠️ Using Surface Web")
        return False
    
    def classify_data(self, data, context=""):
        """Enhanced classification - Fixed regex"""
        patterns = {
            'NAME': r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+){{0,2}}\b',
            'PHONE': r'[\+]?[6-9]\d{{9,11}}',
            'EMAIL': r'\b[\w\.-]+@[a-zA-Z0-9\-\.]+\.[a-zA-Z]{{2,}}\b',
            'PINCODE': r'\b[1-9]\d{{5}}\b',
            'PAN': r'[A-Z]{{5}}[0-9]{{4}}[A-Z]',
            'AADHAAR': r'\b\d{{12}}\b'
        }
        full_text = (data + ' ' + context).lower()
        for cat, pattern in patterns.items():
            matches = re.findall(pattern, full_text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                clean = re.sub(r'[^\w\s@.\-+]', '', str(match).strip())
                if len(clean) > 3:
                    return cat, clean[:70]
        return "DATA", data[:70]
    
    def scan_url(self, url, source, engine="WEB", use_tor=False):
        """Fixed URL scanner"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            session = self.tor_session if use_tor and self.tor_session else requests
            resp = session.get(url, headers=headers, timeout=25, allow_redirects=True)
            
            if resp.status_code == 200:
                text_lower = resp.text.lower()
                if self.target.lower() in text_lower:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    title = soup.title.string.strip() if soup.title else "No title"
                    context = f"{title} {resp.text[:2000]}"
                    
                    cat, clean_data = self.classify_data(self.target, context)
                    self.print_result(cat, clean_data, source, engine, url, "TOR" if use_tor else "🌐")
        except:
            pass
    
    def darkweb_scan(self):
        print(f"{Fore.RED}🕳️ DARKWEB")
        dark_sites = [
            ("Ahmia", f"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={urllib.parse.quote(self.target)}"),
            ("Torch", f"http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/?q={urllib.parse.quote(self.target)}")
        ]
        threads = []
        for name, url in dark_sites:
            t = Thread(target=self.scan_url, args=(url, name, "DARKWEB", True), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(60)
    
    def government_scan(self):
        print(f"{Fore.RED}🏛️ GOVERNMENT")
        govt_sites = [
            ("IncomeTax", f"https://incometaxindia.gov.in/search-result?search={urllib.parse.quote(self.target)}"),
            ("EPFO", f"https://unifiedportal-mem.epfindia.gov.in/memberinterface/#/search?q={urllib.parse.quote(self.target)}"),
            ("GST", f"https://www.gst.gov.in/search?query={urllib.parse.quote(self.target)}"),
            ("MCA", f"https://www.mca.gov.in/content/mca/global/en/search.html?q={urllib.parse.quote(self.target)}")
        ]
        threads = []
        for name, url in govt_sites:
            t = Thread(target=self.scan_url, args=(url, name, "GOVT"), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(40)
    
    def companies_scan(self):
        print(f"{Fore.RED}🏢 COMPANIES")
        corp_sites = [
            ("ZaubaCorp", f"https://www.zaubacorp.com/search?q={urllib.parse.quote(self.target)}"),
            ("IndiaMart", f"https://dir.indiamart.com/search.mp?ss={urllib.parse.quote(self.target)}"),
            ("JustDial", f"https://www.justdial.com/search?q={urllib.parse.quote(self.target)}"),
            ("Tofler", f"https://www.tofler.in/search?q={urllib.parse.quote(self.target)}")
        ]
        threads = []
        for name, url in corp_sites:
            t = Thread(target=self.scan_url, args=(url, name, "CORP"), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(40)
    
    def run_full_scan(self):
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 OUTPUT FOLDER: {TARGET_FOLDER}")
        print("=" * 90 + "\n")
        
        self.tor_init()
        time.sleep(3)
        
        # ALL SCANS - FULL SPECTRUM
        scans = [
            self.breach_scan,        # NEW: All breach data
            self.social_media_scan,
            self.photo_scan,
            self.darkweb_scan,
            self.government_scan,
            self.companies_scan,
            self.git_tools_scan,
            self.kali_tool_scan
        ]
        
        threads = [Thread(target=scan, daemon=True) for scan in scans]
        for t in threads: t.start()
        for t in threads: t.join(1800)  # 30 min total
        
        print(f"\n{Fore.RED}🎉 KHALID HUSAIN786 v85.4 COMPLETE!")
        print(f"{Fore.GREEN}📄 MASTER PDF: {self.pdf_file}")
        print(f"{Fore.CYAN}✨ {len(self.results)} HITS • CHECK ./Target/")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target>")
        print(f"{Fore.YELLOW}Example: python3 khalid-osint.py 'john.doe@example.com'")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv854()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()
