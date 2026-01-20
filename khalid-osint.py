#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.7 - TERMINAL → PDF EXACT MATCH
REAL DATA FROM ALL SOURCES • NO LIMITS • PERFECT PDF
"""

import os
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
    from weasyprint import HTML
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

init(autoreset=True)
print_lock = Lock()

TARGET_FOLDER = "./Target"
os.makedirs(TARGET_FOLDER, exist_ok=True)

class KhalidHusain786OSINTv857:
    def __init__(self):
        self.target = ""
        self.results = []
        self.terminal_output = []
        self.company_intel = {}
        self.target_pdf = None
        
    def banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}      KHALID HUSAIN786 v85.7 - REAL OSINT ENGINE     {Fore.RED}║
{Fore.RED}║{Fore.CYAN}     WEB•BREACHES•SOCIAL•PASTE•GITHUB•ALL SOURCES  {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}     PASSWORDS•EMAILS•PHONES•TOKENS•DOMAINS      {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
        self.terminal_output.append("KHALID HUSAIN786 v85.7 - REAL OSINT ENGINE")
    
    def pii_patterns(self):
        return {
            '🔐 RAW PASS': r'(?:passw[o0]rd|pwd|token|key|secret)[:\s]*["\']?([^\s"\'\n]{4,50})["\']?',
            '🔑 HASH': r'\b[A-Fa-f0-9]{32,128}\b',
            '📧 EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '👤 USERNAME': r'@[A-Za-z0-9_]{3,30}|[A-Za-z0-9_]{3,30}(?:@[A-Za-z0-9_]+)?',
            '🏢 COMPANY': r'(?:inc|corp|ltd|llc|plc|co\.?\s?)(?:\.)?[A-Za-z\s\.\-]{2,50}',
            '📞 PHONE': r'[\+]?[1-9]\d{7,15}',
            '🌐 DOMAIN': r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}',
            '₿ BITCOIN': r'bc1[A-Za-z9]{39,59}|1[0-9A-Za-z]{25,34}|3[0-9A-Za-z]{25,34}'
        }
    
    def extract_pii(self, text):
        pii_data = {}
        patterns = self.pii_patterns()
        
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                pii_data[pii_type] = matches[0][:50]
        
        return pii_data if pii_data else {'TARGET': self.target}
    
    def print_result(self, category, data, source, engine, link=""):
        with print_lock:
            emojis = {"BREACH": "💥", "PASTE": "📋", "GITHUB": "🐙", "SOCIAL": "📱", "DOMAIN": "🌐"}
            emoji = emojis.get(category, "🔍")
            
            output_lines = []
            output_lines.append(f"✓ [{emoji}] {Fore.CYAN}{category:10} | {Fore.YELLOW}{source:14} | {Fore.MAGENTA}{engine}")
            
            if isinstance(data, dict):
                for pii_type, pii_value in data.items():
                    color = Fore.RED if any(x in pii_type for x in ['PASS', 'HASH', 'KEY']) else Fore.WHITE
                    output_lines.append(f"   🆔 {Fore.CYAN}{pii_type:12}: {color}{pii_value}")
            else:
                output_lines.append(f"   🆔 {Fore.RED}→ {data}")
            
            if link:
                output_lines.append(f"   🔗 {Fore.BLUE}{link[:60]}...")
            output_lines.append("")
            
            for line in output_lines:
                print(line)
            
            clean_lines = [re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', line) for line in output_lines]
            self.terminal_output.extend(clean_lines)
            
            self.results.append({
                'category': category, 'data': data, 'source': source,
                'engine': engine, 'link': link or f"https://google.com/search?q={urllib.parse.quote(self.target)}+{urllib.parse.quote(source)}"
            })
    
    def search_google_dorks(self, dorks):
        """REAL Google Dorks - pulls actual web data"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for dork, category in dorks.items():
            try:
                query = f"{self.target} {dork}"
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                resp = requests.get(url, headers=headers, timeout=10)
                
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    results = soup.find_all('div', class_='g')[:3]  # Top 3 results
                    
                    for i, result in enumerate(results):
                        title = result.find('h3')
                        link = result.find('a', href=True)
                        if title and link:
                            title_text = title.get_text()
                            pii = self.extract_pii(title_text + " " + link['href'])
                            if pii:
                                self.print_result(category, pii, f"Google#{i+1}", "DORKS", link['href'])
            except:
                continue
    
    def check_haveibeenpwned(self):
        """Check HIBP for breaches"""
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"
            headers = {'User-Agent': 'KhalidOSINT', 'hibp-api-key': ''}
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                breaches = resp.json()
                for breach in breaches[:5]:
                    self.print_result("BREACH", {'💥 BREACH': breach['Name']}, "HIBP", "BREACH", f"https://haveibeenpwned.com/{breach['Name']}")
            elif resp.status_code == 404:
                self.print_result("BREACH", {'✅ CLEAN': 'No breaches found'}, "HIBP", "BREACH")
        except:
            self.print_result("BREACH", {'❌ ERROR': 'HIBP unavailable'}, "HIBP", "BREACH")
    
    def github_search(self):
        """Search GitHub for leaks"""
        try:
            url = f"https://github.com/search?q={urllib.parse.quote(self.target)}+password&type=code"
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = requests.get(url, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                code_blocks = soup.find_all('div', class_='d')
                for block in code_blocks[:3]:
                    text = block.get_text()
                    pii = self.extract_pii(text)
                    if pii:
                        self.print_result("GITHUB", pii, "Code Search", "GITHUB", url)
        except:
            pass
    
    def paste_sites(self):
        """Check paste sites"""
        sites = [
            f"https://pastebin.com/search?q={urllib.parse.quote(self.target)}",
            f"https://searchpaste.org/?q={urllib.parse.quote(self.target)}"
        ]
        
        for site in sites:
            try:
                resp = requests.get(site, timeout=10)
                pii = self.extract_pii(resp.text)
                if pii:
                    self.print_result("PASTE", pii, site.split('/')[2], "PASTE", site)
            except:
                continue
    
    def social_search(self):
        """Social media footprints"""
        platforms = [
            ("Twitter", f"https://twitter.com/search?q={urllib.parse.quote(self.target)}"),
            ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}"),
            ("FB", f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}")
        ]
        
        for platform, url in platforms:
            try:
                resp = requests.get(url, timeout=10)
                pii = self.extract_pii(resp.text)
                if pii:
                    self.print_result("SOCIAL", pii, platform, "SOCIAL", url)
            except:
                continue
    
    def run_full_scan(self):
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 OUTPUT: {TARGET_FOLDER}/")
        print("="*90)
        
        self.terminal_output.extend([f"🎯 TARGET: {self.target}", f"📁 OUTPUT: {TARGET_FOLDER}/", "="*90])
        
        # 🔥 REAL SCANS FROM ALL SOURCES
        print(f"{Fore.CYAN}🔍 Google Dorks...")
        dorks = {
            "password filetype:txt": "PASS",
            "email | phone": "CONTACT", 
            "api key | token": "APIKEY",
            "intext:admin": "ADMIN"
        }
        self.search_google_dorks(dorks)
        
        print(f"{Fore.CYAN}💥 Breach Check...")
        self.check_haveibeenpwned()
        
        print(f"{Fore.CYAN}🐙 GitHub Leaks...")
        self.github_search()
        
        print(f"{Fore.CYAN}📋 Paste Sites...")
        self.paste_sites()
        
        print(f"{Fore.CYAN}📱 Social Footprint...")
        self.social_search()
        
        print(f"\n{Fore.RED}✅ FULL SCAN COMPLETE! {len(self.results)} records found!")
        print(f"{Fore.GREEN}📄 Generating PDF...")
        
        self.update_pdf()
        print(f"{Fore.CYAN}🎉 Check {TARGET_FOLDER}/ for results!")

    def update_pdf(self):
        if not self.results:
            print(f"{Fore.RED}❌ No results found!")
            return
            
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:40]
        self.target_pdf = f"{TARGET_FOLDER}/{clean_target}_OSINTv857.pdf"
        
        html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>{self.target} - KHALID OSINT v85.7 ({len(self.results)} Records)</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Roboto Mono',monospace;background:#0a0e17;color:#e6edf3;font-size:11px;line-height:1.4;padding:25px;}}
h1{{font-size:22px;color:#00d4aa;text-align:center;margin-bottom:30px;letter-spacing:2px;}}
.terminal{{background:#1a2332;border:2px solid #2d4059;border-radius:20px;padding:30px;max-height:70vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.8);}}
.terminal-line{{margin:4px 0;padding:8px 12px;border-radius:8px;background:rgba(26,35,50,0.6);font-size:10.5px;white-space:pre-wrap;border-left:4px solid #00d4aa;}}
.stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:20px;margin:25px 0;}}
.stat-card{{text-align:center;padding:20px;background:#1a2332;border-radius:15px;border:2px solid #00d4aa;box-shadow:0 10px 30px rgba(0,0,0,0.5);}}
.stat-number{{font-size:28px;font-weight:700;color:#00d4aa;margin-bottom:8px;}}
.pii-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:20px;margin:30px 0;}}
.pii-card{{background:#1a2332;padding:25px;border-radius:20px;border-left:6px solid #00d4aa;box-shadow:0 12px 40px rgba(0,0,0,0.6);}}
.pii-type{{font-weight:900;color:#00d4aa;font-size:12px;margin-bottom:15px;text-transform:uppercase;}}
.pii-value{{background:#0a0e17;padding:18px;border-radius:15px;font-size:11px;font-weight:600;word-break:break-word;border:2px solid #2d4059;}}
.hash-value{{border-left-color:#ff4757;background:rgba(255,71,87,0.1);color:#ff9aa2;}}
a{{color:#00d4aa;text-decoration:none;font-weight:700;padding:8px 16px;background:#2d4059;border-radius:20px;display:inline-block;margin-top:10px;}}
a:hover{{background:#00d4aa;color:#000;}}
</style></head><body>'''
        
        html += f'<h1>🎯 {self.target} - REAL OSINT ({len(self.results)} Records)</h1>'
        
        creds_count = len([r for r in self.results if any(x in str(r.get('data','')).upper() for x in ['PASS','HASH','KEY'])])
        html += f'''
<div class="stats-grid">
<div class="stat-card"><div class="stat-number">{len(self.results)}</div><div>RECORDS</div></div>
<div class="stat-card"><div class="stat-number">{creds_count}</div><div>CREDS</div></div>
<div class="stat-card"><div class="stat-number">{datetime.now().strftime('%H:%M:%S')}</div><div>COMPLETE</div></div>
</div>
'''
        
        html += '<div class="terminal"><h2 style="color:#ff6b6b;">💻 LIVE TERMINAL OUTPUT</h2>'
        for line in self.terminal_output[-150:]:
            is_cred = any(x in line.upper() for x in ['PASS', 'HASH', 'KEY'])
            html += f'<div class="terminal-line {"hash-value" if is_cred else ""}">{line}</div>'
        html += '</div>'
        
        html += f'<h2 style="color:#ff6b6b;">🆔 PII EXTRACTED ({len(self.results)})</h2><div class="pii-grid">'
        for result in self.results[-25:]:
            if isinstance(result['data'], dict):
                for pii_type, pii_value in result['data'].items():
                    is_hash = any(x in pii_type for x in ['HASH', 'PASS'])
                    html += f'''
<div class="pii-card">
<div class="pii-type">{"🔴" if is_hash else "🔵"} {pii_type}</div>
<div class="pii-value {'hash-value' if is_hash else ''}">{pii_value}</div>
<a href="{result['link']}" target="_blank">🔗 SOURCE</a>
</div>'''
        html += '</div></body></html>'
        
        try:
            if PDF_AVAILABLE:
                HTML(string=html).write_pdf(self.target_pdf)
                print(f"{Fore.GREEN}✅ PDF SAVED: {self.target_pdf}")
            else:
                html_file = self.target_pdf.replace('.pdf', '.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"{Fore.YELLOW}✅ HTML SAVED: {html_file}")
                print(f"{Fore.CYAN}💡 pip install weasyprint for PDF output")
        except Exception as e:
            print(f"{Fore.RED}❌ Save error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target>")
        print(f"{Fore.YELLOW}Example: python3 khalid-osint.py john.doe@gmail.com")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv857()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()
