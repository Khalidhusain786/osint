#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.4 - SINGLE TARGET FOLDER + SINGLE PDF PER TARGET
FIXED PDF RENDERING + TARGET ONLY DATA + NO CODE CHANGES
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
        
    def banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}                KHALID HUSAIN786 v85.4                 {Fore.RED}║
{Fore.RED}║{Fore.CYAN}   FULL SPECTRUM + BREACH DATA + TARGET ONLY DATA       {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}     FIXED PDF • SINGLE TARGET • ./Target/ OUTPUT   {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def breach_scan(self):
        print(f"{Fore.RED}💥 BREACH DATA")
        breach_sources = [
            ("HIBP", f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"),
            ("Dehashed", f"https://dehashed.com/search?query={urllib.parse.quote(self.target)}"),
            ("LeakCheck", f"https://leakcheck.io/api/?key=demo&q={urllib.parse.quote(self.target)}"),
            ("BreachDir", f"https://breachdirectory.org/search?email={urllib.parse.quote(self.target)}"),
            ("Snusbase", f"https://snusbase.com/search?q={urllib.parse.quote(self.target)}"),
            ("IntelX", f"https://intelx.io/search?term={urllib.parse.quote(self.target)}&tab=emails")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "BREACH"), daemon=True) for name, url in breach_sources]
        for t in threads: t.start()
        for t in threads: t.join(30)
    
    def kali_tool_scan(self):
        print(f"{Fore.RED}⚡ KALI TOOLS")
        kali_tools = [
            ("theHarvester", ["theHarvester", "-d", self.target, "-b", "google,bing", "-l", "50"]),
            ("dnsrecon", ["dnsrecon", "-d", self.target]),
            ("sublist3r", ["sublist3r", "-d", self.target])
        ]
        for tool_name, cmd in kali_tools:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                self.print_result("KALI", self.target, "Kali", tool_name, f"file://{TARGET_FOLDER}/{self.target}_{tool_name.lower()}.txt", "⚡")
            except:
                pass
    
    def social_media_scan(self):
        print(f"{Fore.RED}📱 SOCIAL")
        social = [
            ("Facebook", f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}"),
            ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}"),
            ("Twitter", f"https://twitter.com/search?q={urllib.parse.quote(self.target)}"),
            ("Instagram", f"https://www.instagram.com/explore/search/keyword/?q={urllib.parse.quote(self.target)}"),
            ("Reddit", f"https://www.reddit.com/search/?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "SOCIAL"), daemon=True) for name, url in social]
        for t in threads: t.start()
        for t in threads: t.join(25)
    
    def photo_scan(self):
        print(f"{Fore.RED}📸 IMAGES")
        images = [
            ("Google", f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(self.target)}"),
            ("Yandex", f"https://yandex.com/images/search?text={urllib.parse.quote(self.target)}"),
            ("Bing", f"https://www.bing.com/images/search?q={urllib.parse.quote(self.target)}")
        ]
        threads = [Thread(target=self.scan_url, args=(url, name, "PHOTOS"), daemon=True) for name, url in images]
        for t in threads: t.start()
        for t in threads: t.join(20)
    
    def update_pdf(self):
        if not self.results:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.pdf_file = f"{TARGET_FOLDER}/{self.target}_KhalidHusain786_{timestamp}.pdf"
        
        html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{self.target}</title>
<style>
body {{font-family:Arial,sans-serif;background:#1a1a2e;color:#fff;padding:20px;font-size:12px;line-height:1.4;max-width:100%;margin:0;}}
.header {{background:#16213e;padding:20px;text-align:center;border-radius:10px;margin-bottom:20px;}}
h1 {{font-size:24px;margin:0;color:#ffd700;text-align:center;}}
.stats {{display:flex;justify-content:space-around;margin:20px 0;}}
.stat {{background:rgba(255,255,255,0.1);padding:10px;border-radius:8px;text-align:center;flex:1;margin:0 5px;}}
.grid {{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:15px;}}
.card {{background:rgba(255,255,255,0.08);padding:15px;border-radius:10px;border-left:4px solid #4ecdc4;}}
.cat {{font-weight:bold;color:#ffd700;font-size:11px;margin-bottom:5px;}}
.data {{color:#fff;font-size:12px;margin-bottom:8px;}}
.link {{display:block;padding:8px;background:#4ecdc4;color:#000;text-decoration:none;border-radius:5px;font-weight:bold;text-align:center;font-size:11px;}}
.link:hover {{background:#45b7d1;}}
.source {{font-size:10px;color:#aaa;}}
@media print {{body {{font-size:10px;}} .grid {{grid-template-columns:repeat(3,1fr);}}}}
</style></head><body>
<div class="header"><h1>🔍 TARGET: {self.target}</h1>
<div class="stats">
<div class="stat"><strong>{self.target}</strong><div>Target</div></div>
<div class="stat"><strong>{len(self.results)}</strong><div>Hits</div></div>
<div class="stat">{datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
</div></div>
<div class="grid">'''

        for result in self.results[-30:]:  # Last 30 only
            cat_class = result['category'].lower()
            html += f'''<div class="card">
<div class="cat">{result['category']}</div>
<div class="data">{result['data']}</div>
<div class="source">{result['source']} • {result['engine']}</div>
<a href="{result['link']}" target="_blank" class="link">🔗 OPEN</a>
</div>'''
        
        html += '</div></body></html>'
        
        try:
            from weasyprint import HTML
            HTML(string=html, base_url='').write_pdf(
                self.pdf_file, 
                stylesheets=None,
                optimize_images=True
            )
            print(f"{Fore.GREEN}📄 PDF FIXED: {self.pdf_file}")
        except:
            html_file = self.pdf_file.replace('.pdf', '.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"{Fore.YELLOW}📄 HTML: {html_file}")
    
    def print_result(self, category, data, source, engine, link="", network="🌐"):
        with print_lock:
            emojis = {"BREACH": "💥", "SOCIAL": "📱", "KALI": "⚡", "PHOTOS": "📸"}
            emoji = emojis.get(category, "🌐")
            print(f"{Fore.GREEN}✓ [{emoji}] {Fore.CYAN}{category:10} | {Fore.YELLOW}{source:12} | {Fore.MAGENTA}{engine}")
            print(f"   {Fore.RED}→ {data}{Style.RESET_ALL}")
            if link: print(f"   {Fore.BLUE}🔗 {link[:80]}...")
            
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
                return True
        except: pass
        return False
    
    def scan_url(self, url, source, engine="WEB"):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            session = self.tor_session if self.tor_session else requests
            resp = session.get(url, headers=headers, timeout=20)
            if resp.status_code == 200 and self.target.lower() in resp.text.lower():
                self.print_result(engine, self.target, source, engine, url)
        except: pass
    
    def run_full_scan(self):
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 FOLDER: {TARGET_FOLDER}")
        print("="*70)
        
        self.tor_init()
        
        scans = [self.breach_scan, self.social_media_scan, self.photo_scan, self.kali_tool_scan]
        threads = [Thread(target=scan, daemon=True) for scan in scans]
        for t in threads: t.start()
        for t in threads: t.join(900)
        
        print(f"\n{Fore.RED}🎉 SCAN COMPLETE!")
        print(f"{Fore.GREEN}📄 PDF: {self.pdf_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target>")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv854()
    osint.target = sys.argv[1]
    osint.run_full_scan()
