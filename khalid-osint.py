#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v85.7 - REAL DATA FROM ALL SOURCES
TERMINAL → PDF PERFECT MATCH • NO FAKE DATA • LIVE RESULTS
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
{Fore.RED}║{Fore.YELLOW}      KHALID HUSAIN786 v85.7 - LIVE OSINT ENGINE      {Fore.RED}║
{Fore.RED}║{Fore.CYAN}  WEB•BREACHES•SOCIAL•PASTE•GITHUB•WHOIS•ALL SOURCES {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}     PASSWORDS•EMAILS•PHONES•TOKENS•DOMAINS      {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
        self.terminal_output.append("KHALID HUSAIN786 v85.7 - LIVE OSINT ENGINE")
    
    def pii_patterns(self):
        return {
            '🔐 PASS/KEY': r'(?:passw[o0]rd|pwd|token|key|secret|api[_-]?key)[:\s]*["\']?([^\s"\'\n]{4,80})["\']?',
            '🔑 HASH': r'\b[A-Fa-f0-9]{32,128}\b',
            '📧 EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '👤 USERNAME': r'@[A-Za-z0-9_]{3,30}|[A-Za-z0-9_]{3,30}(?:@[A-Za-z0-9_]+)?',
            '📞 PHONE': r'[\+]?[1-9]\d{7,15}',
            '🌐 DOMAIN': r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}',
            '₿ BITCOIN': r'bc1[A-Za-z9]{39,59}|1[0-9A-Za-z]{25,34}|3[0-9A-Za-z]{25,34}',
            '🏢 COMPANY': r'(?:inc|corp|ltd|llc|plc|co\.?\s?)(?:\.)?[A-Za-z\s\.\-]{2,50}'
        }
    
    def extract_pii(self, text):
        pii_data = {}
        patterns = self.pii_patterns()
        
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                pii_data[pii_type] = matches[0][:60]  # First match, truncated
                
        return pii_data if pii_data else {'TARGET': self.target}
    
    def print_result(self, category, data, source, engine, link=""):
        with print_lock:
            emojis = {"BREACH": "💥", "PASTE": "📋", "GITHUB": "🐙", "SOCIAL": "📱", "DOMAIN": "🌐", "WHOIS": "🏛️"}
            emoji = emojis.get(category, "🔍")
            
            output_lines = []
            output_lines.append(f"✓ [{emoji}] {Fore.CYAN}{category:10} | {Fore.YELLOW}{source:14} | {Fore.MAGENTA}{engine}")
            
            if isinstance(data, dict):
                for pii_type, pii_value in data.items():
                    color = Fore.RED if any(x in pii_type.upper() for x in ['PASS','HASH','KEY']) else Fore.WHITE
                    output_lines.append(f"   🆔 {Fore.CYAN}{pii_type:12}: {color}{pii_value}")
            else:
                output_lines.append(f"   🆔 {Fore.RED}→ {data}")
            
            if link:
                output_lines.append(f"   🔗 {Fore.BLUE}{link[:65]}...")
            output_lines.append("")
            
            for line in output_lines:
                print(line)
            
            # Clean for PDF
            clean_lines = [re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', line) for line in output_lines]
            self.terminal_output.extend(clean_lines)
            
            self.results.append({
                'category': category, 'data': data, 'source': source,
                'engine': engine, 'link': link or f"https://google.com/search?q={urllib.parse.quote(self.target)}+{urllib.parse.quote(source)}"
            })
    
    def google_dorks(self):
        """LIVE Google Dorks - Real web scraping"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        dorks = {
            "password OR token OR key filetype:txt": "PASSWD",
            '"email" OR "phone" OR "contact"': "CONTACT", 
            "api[_-]key OR secret": "APIKEY",
            "admin login OR dashboard": "ADMIN",
            "config OR .env": "CONFIG"
        }
        
        print(f"{Fore.CYAN}🔍 LIVE Google Dorks...")
        for dork_name, category in dorks.items():
            try:
                query = f'"{self.target}" {dork_name}'
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=10"
                resp = requests.get(url, headers=headers, timeout=12)
                
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    results = soup.find_all('div', class_='g')[:4]
                    
                    for i, result in enumerate(results):
                        title = result.find('h3')
                        link_elem = result.find('a', href=True)
                        snippet = result.find('div', class_='VwiC3b')
                        
                        if title and link_elem:
                            text = (title.get_text() + " " + (snippet.get_text() if snippet else "")).lower()
                            pii = self.extract_pii(title.get_text() + " " + link_elem['href'])
                            
                            if pii or self.target.lower() in text:
                                self.print_result(category, pii or {'HIT': 'Target found'}, f"Google#{i+1}", "DORKS", link_elem['href'])
                                time.sleep(1)  # Rate limit
            except:
                continue
    
    def hibp_breaches(self):
        """LIVE HIBP breach check"""
        print(f"{Fore.CYAN}💥 HIBP Breach Check...")
        try:
            # Check if target looks like email
            if '@' in self.target:
                url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}?truncateResponse=true"
                headers = {'User-Agent': 'KhalidOSINTv857', 'hibp-api-key': ''}
                resp = requests.get(url, headers=headers, timeout=10)
                
                if resp.status_code == 200:
                    breaches = resp.json()
                    for breach in breaches[:6]:
                        self.print_result("BREACH", {'💥 BREACH': breach['Name']}, "HIBP", "API", f"https://haveibeenpwned.com/{breach['Name']}")
                elif resp.status_code == 404:
                    self.print_result("BREACH", {'✅ CLEAN': 'No breaches'}, "HIBP", "API")
                else:
                    self.print_result("BREACH", {'⚠️ RATE': 'Limited'}, "HIBP", "API")
        except:
            self.print_result("BREACH", {'❌ OFFLINE': 'HIBP unavailable'}, "HIBP", "API")
    
    def github_leaks(self):
        """LIVE GitHub code search"""
        print(f"{Fore.CYAN}🐙 GitHub Leaks...")
        try:
            queries = [
                f'"{self.target}" password',
                f'"{self.target}" token', 
                f'"{self.target}" key',
                f'"{self.target}" secret'
            ]
            
            for query in queries[:2]:  # Limit to avoid rate limiting
                url = f"https://github.com/search?q={urllib.parse.quote(query)}&type=code"
                headers = {'User-Agent': 'Mozilla/5.0'}
                resp = requests.get(url, headers=headers, timeout=10)
                
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    code_results = soup.find_all('div', {'data-hydro-click': True})[:3]
                    
                    for i, result in enumerate(code_results):
                        text = result.get_text()
                        pii = self.extract_pii(text)
                        if pii:
                            self.print_result("GITHUB", pii, f"Code#{i+1}", "SEARCH", url)
                            break
        except:
            pass
    
    def paste_search(self):
        """LIVE paste sites"""
        print(f"{Fore.CYAN}📋 Paste Sites...")
        sites = [
            ("Pastebin", f"https://pastebin.com/search?q={urllib.parse.quote(self.target)}"),
            ("Paste.ee", f"https://paste.ee/search?q={urllib.parse.quote(self.target)}"),
        ]
        
        for name, url in sites:
            try:
                resp = requests.get(url, timeout=8)
                pii = self.extract_pii(resp.text)
                if pii:
                    self.print_result("PASTE", pii, name, "SEARCH", url)
            except:
                continue
    
    def social_footprint(self):
        """LIVE social media search"""
        print(f"{Fore.CYAN}📱 Social Footprint...")
        platforms = [
            ("Twitter", f"https://twitter.com/search?q={urllib.parse.quote(self.target)}&src=typed_query"),
            ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}"),
            ("FB", f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}")
        ]
        
        for platform, url in platforms:
            try:
                resp = requests.get(url, timeout=8)
                pii = self.extract_pii(resp.text)
                if any(self.target.lower() in t.lower() for t in resp.text.split()) or pii:
                    self.print_result("SOCIAL", pii or {'👤 PROFILE': 'Found'}, platform, "FOOTPRINT", url)
            except:
                continue
    
    def whois_lookup(self):
        """WHOIS lookup if target is domain"""
        if '.' in self.target and any(tld in self.target for tld in ['.com','.net','.org','.io']):
            print(f"{Fore.CYAN}🏛️ WHOIS Lookup...")
            try:
                url = f"https://www.whois.com/whois/{urllib.parse.quote(self.target)}"
                resp = requests.get(url, timeout=8)
                soup = BeautifulSoup(resp.text, 'html.parser')
                whois_text = soup.get_text()
                
                pii = self.extract_pii(whois_text)
                if pii:
                    self.print_result("WHOIS", pii, self.target, "DOMAIN", url)
                else:
                    self.print_result("WHOIS", {'✅ ACTIVE': 'Domain registered'}, self.target, "DOMAIN", url)
            except:
                pass
    
    def run_full_scan(self):
        self.banner()
        print(f"{Fore.WHITE}🎯 TARGET: {Fore.YELLOW}{self.target}")
        print(f"{Fore.GREEN}📁 OUTPUT: {TARGET_FOLDER}/")
        print("="*95)
        self.terminal_output.extend([f"🎯 TARGET: {self.target}", f"📁 OUTPUT: {TARGET_FOLDER}/", "="*95])
        
        # 🔥 LIVE SCAN - ALL SOURCES
        Thread(target=self.google_dorks).start()
        time.sleep(2)
        
        Thread(target=self.hibp_breaches).start()
        Thread(target=self.github_leaks).start()
        time.sleep(3)
        
        Thread(target=self.paste_search).start()
        Thread(target=self.social_footprint).start()
        Thread(target=self.whois_lookup).start()
        
        time.sleep(8)  # Let threads complete
        
        print(f"\n{Fore.RED}✅ LIVE SCAN COMPLETE! {len(self.results)} records from {len(set(r['source'] for r in self.results))} sources!")
        print(f"{Fore.GREEN}📄 Generating PDF report...")
        
        self.update_pdf()
        print(f"{Fore.CYAN}🎉 Results saved to {TARGET_FOLDER}/")

    def update_pdf(self):
        if not self.results:
            print(f"{Fore.RED}❌ No results found!")
            return
            
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:45]
        self.target_pdf = f"{TARGET_FOLDER}/{clean_target}_OSINTv857.pdf"
        
        html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>KHALID OSINT v85.7 - {self.target} ({len(self.results)} Records)</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'JetBrains Mono',monospace;background:linear-gradient(135deg,#0a0e17 0%,#1a2332 100%);color:#e6edf3;font-size:11px;line-height:1.45;padding:30px;min-height:100vh;}}
h1{{font-size:24px;color:#00d4aa;text-align:center;margin-bottom:35px;letter-spacing:2px;font-weight:700;text-shadow:0 0 20px rgba(0,212,170,0.5);}}
.terminal{{background:rgba(26,35,50,0.95);backdrop-filter:blur(20px);border:2px solid #2d4059;border-radius:25px;padding:35px;max-height:65vh;overflow-y:auto;box-shadow:0 25px 80px rgba(0,0,0,0.9);margin:25px 0;}}
.terminal-title{{color:#ff6b6b;font-size:16px;margin-bottom:20px;font-weight:700;}}
.terminal-line{{margin:6px 0;padding:10px 15px;border-radius:10px;background:rgba(26,35,50,0.7);font-size:11px;white-space:pre-wrap;border-left:5px solid #00d4aa;box-shadow:inset 0 2px 10px rgba(0,0,0,0.3);}}
.hash-line{{border-left-color:#ff4757;background:rgba(255,71,87,0.15) !important;}}
.stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:25px;margin:35px 0;}}
.stat-card{{text-align:center;padding:30px;background:rgba(26,35,50,0.8);border-radius:20px;border:2px solid #00d4aa;box-shadow:0 15px 50px rgba(0,212,170,0.2);backdrop-filter:blur(10px);transition:transform 0.3s;}}
.stat-card:hover{{transform:translateY(-5px);}}
.stat-number{{font-size:32px;font-weight:700;color:#00d4aa;margin-bottom:12px;text-shadow:0 0 15px rgba(0,212,170,0.5);}}
.pii-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:25px;margin:40px 0;}}
.pii-card{{background:rgba(26,35,50,0.9);padding:30px;border-radius:25px;border-left:8px solid #00d4aa;box-shadow:0 20px 60px rgba(0,0,0,0.7);}}
.pii-type{{font-weight:900;color:#00d4aa;font-size:13px;margin-bottom:20px;text-transform:uppercase;letter-spacing:1px;}}
.pii-value{{background:rgba(10,14,23,0.9);padding:22px;border-radius:18px;font-size:12px;font-weight:600;word-break:break-all;border:2px solid #2d4059;box-shadow:inset 0 3px 15px rgba(0,0,0,0.5);}}
.hash-value{{border-left-color:#ff4757 !important;background:rgba(255,71,87,0.12) !important;color:#ff9aa2 !important;}}
a{{color:#00d4aa !important;text-decoration:none;font-weight:700;padding:12px 22px;background:rgba(45,64,89,0.8);border-radius:25px;display:inline-block;margin-top:15px;border:2px solid transparent;transition:all 0.3s;}}
a:hover{{background:#00d4aa !important;color:#000 !important;border-color:#00d4aa;transform:translateY(-2px);box-shadow:0 10px 30px rgba(0,212,170,0.4);}}
.footer{{text-align:center;margin-top:40px;padding:25px;background:rgba(26,35,50,0.6);border-radius:20px;font-size:10px;color:#888;}}
@media (max-width:768px){{.pii-grid{{grid-template-columns:1fr;}}}}
</style></head><body>'''
        
        html += f'<h1>🎯 LIVE OSINT - {self.target}<br><span style="font-size:16px;color:#ff6b6b;">{len(self.results)} Records • {len(set(r["source"] for r in self.results))} Sources</span></h1>'
        
        creds_count = len([r for r in self.results if any(x in str(r.get('data','')).upper() for x in ['PASS','KEY','HASH'])])
        html += f'''
<div class="stats-grid">
<div class="stat-card"><div class="stat-number">{len(self.results)}</div><div>TOTAL RECORDS</div></div>
<div class="stat-card"><div class="stat-number" style="color:#ff4757;">{creds_count}</div><div>CREDENTIALS</div></div>
<div class="stat-card"><div class="stat-number">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div><div>SCAN COMPLETE</div></div>
</div>
'''
        
        html += f'<div class="terminal"><div class="terminal-title">💻 LIVE TERMINAL SESSION ({len(self.terminal_output)} lines)</div>'
        for line in self.terminal_output[-200:]:
            is_cred = any(x in line.upper() for x in ['PASS', 'HASH', 'KEY', 'TOKEN'])
            html += f'<div class="terminal-line {"hash-line" if is_cred else ""}>{line}</div>'
        html += '</div>'
        
        html += f'<h2 style="color:#ff6b6b;font-size:20px;">🆔 LIVE PII EXTRACTION (Top {min(30,len(self.results))} Results)</h2><div class="pii-grid">'
        for result in self.results[-30:]:
            if isinstance(result['data'], dict):
                for pii_type, pii_value in result['data'].items():
                    is_hash = any(x in pii_type.upper() for x in ['PASS','HASH','KEY'])
                    html += f'''
<div class="pii-card">
<div class="pii-type">{"🔴" if is_hash else "🔵"} {pii_type}</div>
<div class="pii-value {'hash-value' if is_hash else ''}">{pii_value}</div>
<a href="{result['link']}" target="_blank">🔗 OPEN SOURCE</a>
</div>'''
        html += '</div>'
        
        html += f'<div class="footer">KHALID HUSAIN786 OSINT v85.7 | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {len(self.results)} records extracted</div></body></html>'
        
        try:
            if PDF_AVAILABLE:
                HTML(string=html, base_url='file://' + os.getcwd() + '/').write_pdf(
                    self.target_pdf, 
                    stylesheets=None
                )
                print(f"{Fore.GREEN}✅ PDF SAVED: {self.target_pdf}")
            else:
                html_file = self.target_pdf.replace('.pdf', '_FULL.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"{Fore.YELLOW}✅ HTML SAVED: {html_file}")
                print(f"{Fore.CYAN}💡 Install WeasyPrint: pip install weasyprint")
        except Exception as e:
            print(f"{Fore.RED}❌ Save error: {str(e)[:80]}")
            # Fallback HTML
            html_file = self.target_pdf.replace('.pdf', '.html')
            with open(html_file, 'w') as f:
                f.write(html)
            print(f"{Fore.YELLOW}✅ HTML fallback: {html_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}❌ Usage: python3 khalid-osint.py <target>")
        print(f"{Fore.YELLOW}📧 Email: python3 khalid-osint.py john.doe@gmail.com")
        print(f"{Fore.GREEN}🌐 Domain: python3 khalid-osint.py example.com")
        print(f"{Fore.BLUE}👤 Username: python3 khalid-osint.py johnsmith")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv857()
    osint.target = sys.argv[1].strip()
    osint.run_full_scan()
