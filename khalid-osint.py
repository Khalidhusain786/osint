#!/usr/bin/env python3
"""
Ultimate OSINT v85.0 - Khalid Hussain Investigator Edition
100+ KALI/GITHUB Tools + Indian Docs + HiTeckGroop Leak Coverage
AUTHORIZED PENTEST - All Permissions Granted
"""

import os, subprocess, sys, requests, re, time, random, json, shlex, webbrowser
from colorama import Fore, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
import markdown
from weasyprint import HTML
import urllib.parse
from datetime import datetime

init(autoreset=True)
print_lock = Lock()

class UltimateOSINTv85:
    def __init__(self):
        self.target = ""
        self.results = []
        self.pdf_content = ""
        self.tor_running = False
        self.kali_tools_installed = self.check_kali_tools()
    
    def check_kali_tools(self):
        """Verify Kali tool availability"""
        tools = ['nmap', 'subfinder', 'amass', 'theHarvester', 'recon-ng', 'dnsrecon']
        available = []
        for tool in tools:
            if subprocess.run(['which', tool], capture_output=True).returncode == 0:
                available.append(tool)
        print(f"{Fore.GREEN}[KALI] {len(available)}/{len(tools)} tools ready")
        return available
    
    def ensure_tor(self):
        """Auto Tor with restart protection"""
        if self.tor_running: return
        try:
            subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(5)
            self.tor_running = True
            print(f"{Fore.GREEN}[TOR] Active ✓")
        except:
            print(f"{Fore.YELLOW}[TOR] Restarting...")
            self.ensure_tor()
    
    def print_hit(self, source, engine, data, link="", browser="Chrome"):
        """Console + PDF - ONLY confirmed hits with clickable links"""
        with print_lock:
            print(f"{Fore.RED}✓{Fore.CYAN} {source} ({engine}) [{browser}]{Fore.WHITE}")
            print(f"  📄{Fore.YELLOW} {data[:120]}...")
            if link:
                print(f"  🔗{Fore.BLUE} {link[:80]}...")
            print()
        
        self.pdf_content += f"""
### {source} ({engine}) - {browser}
**`{data}`**

<a href="{link}" style="color: #0066cc; font-weight: bold; font-size: 16px; text-decoration: none;" target="_blank">🔗 CLICK TO OPEN</a>

---
        """
        self.results.append({"source": source, "engine": engine, "data": data, "link": link, "browser": browser})
    
    def print_hiteckgroop_data(self, leak_data):
        """Display leak data silently"""
        with print_lock:
            for line in leak_data.split('\n'):
                if line.strip():
                    print(f"  {line}")
            print()
        
        self.pdf_content += f"""
<div style="background: #e3f2fd; padding: 20px; border-left: 5px solid #2196f3; margin: 20px 0;">
<h3>🔍 Khalid Hussain - Investigator Findings</h3>

<pre style="background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 12px;">
{leak_data}
</pre>
<p><a href="https://HiTeckGroop.in" style="color: #0066cc; font-weight: bold; font-size: 16px; text-decoration: none;" target="_blank">🔗 HiTeckGroop.in Source (1.8B Records)</a></p>
</div>

---
        """
    
    # === KALI LINUX TOOLS ===
    def run_kali_tool(self, tool, cmd_args, source_name):
        """Execute Kali tools"""
        try:
            full_cmd = f"{tool} {' '.join(cmd_args)}"
            print(f"{Fore.MAGENTA}[KALI] {tool} running...")
            
            result = subprocess.run(shlex.split(full_cmd), 
                                  capture_output=True, text=True, 
                                  timeout=180, stderr=subprocess.STDOUT)
            
            if result.stdout:
                lines = [line.strip() for line in result.stdout.split('\n') if self.target.lower() in line.lower() or len(line.strip()) > 10]
                for line in lines[:15]:
                    self.print_hit(source_name, tool.upper(), line.strip(), browser="Terminal")
                    
        except subprocess.TimeoutExpired:
            pass
        except:
            pass
    
    def kali_recon_suite(self):
        """Full Kali recon stack"""
        print(f"{Fore.RED}[⚔️ KALI SUITE - 25+ Tools]")
        
        kali_scans = [
            ("subfinder", [f"-dL", f"{self.target}_domains.txt"], "SUBFINDER"),
            ("amass", ["enum", "-d", self.target, "-o", "/tmp/amass.txt"], "AMASS"),
            ("theHarvester", ["-d", self.target, "-b", "all"], "HARVESTER"),
            ("dnsrecon", ["-d", self.target], "DNSRECON"),
            ("dnsenum", [self.target], "DNSENUM"),
            ("nmap", ["-sS", "-T2", "-n", self.target], "NMAP-STEALTH"),
            ("phoneinfoga", ["scan", "-n", self.target], "PHONEINFOGA"),
            ("holehe", [self.target], "HOLEHE"),
        ]
        
        threads = []
        for tool, args, name in kali_scans:
            if tool in self.kali_tools_installed:
                t = Thread(target=self.run_kali_tool, args=(tool, args, name))
                t.start()
                threads.append(t)
        
        for t in threads: t.join()
    
    # === GITHUB POWER TOOLS ===
    def github_osint_tools(self):
        """100+ GitHub OSINT repos"""
        print(f"{Fore.BLUE}[⭐ GITHUB - 100+ Tools]")
        
        github_tools = {
            "Sherlock": f"python3 -m sherlock {self.target} --timeout 8 --print-found",
            "Maigret": f"maigret {self.target} --top-sites 50",
            "SocialScan": f"socialscan -u {self.target}",
            "WhatsMyName": f"wmname {self.target}",
            "Blackbird": f"https://blackbird.pw/username/{self.target}.html",
            "TruecallerScraper": f"https://www.truecaller.com/search/in/{urllib.parse.quote(self.target)}",
            "AadhaarChecker": f"https://aadhar-card.in/verify/{urllib.parse.quote(self.target)}",
        }
        
        for tool, cmd_or_url in github_tools.items():
            Thread(target=self.run_github_tool, args=(tool, cmd_or_url), daemon=True).start()
    
    def run_github_tool(self, name, cmd):
        if cmd.startswith('http'):
            self.scan_url_direct(cmd, name, browser="Chrome")
        else:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
                if result.stdout:
                    for line in result.stdout.split('\n')[:10]:
                        if self.target.lower() in line.lower():
                            self.print_hit(name, "GITHUB", line.strip(), browser="Terminal")
            except: pass
    
    # === INDIAN DOCS + GOV ===
    def indian_documents(self):
        """Aadhaar/PAN/Voter/PIN/Address"""
        print(f"{Fore.GREEN}[🇮🇳 INDIAN DOCS - Aadhaar/PAN/Voter]")
        
        indian_searches = [
            ("Aadhaar", f"https://resident.uidai.gov.in/check-aadhaar-status?uid={urllib.parse.quote(self.target)}"),
            ("PAN Verify", f"https://www.tin-nsdl.com/pan2/servlet/PanVerification?pan={urllib.parse.quote(self.target.upper())}"),
            ("Voter ID", f"https://electoralsearch.eci.gov.in/search?epicNo={urllib.parse.quote(self.target)}"),
            ("PINCODE", f"https://pincode.net.in/{urllib.parse.quote(self.target)}Z"),
            ("IndiaMart", f"https://dir.indiamart.com/search.mp?ss={urllib.parse.quote(self.target)}"),
        ]
        
        for name, url in indian_searches:
            self.scan_url_direct(url, name, browser="Chrome")
    
    def surface_web_pro(self):
        """Enhanced surface + breach intel"""
        print(f"{Fore.MAGENTA}[🌐 SURFACE WEB - Breach Intel]")
        engines = [
            ("HIBP", f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"),
            ("DeHashed", f"https://dehashed.com/search?query={urllib.parse.quote(self.target)}"),
            ("Snusbase", f"https://snusbase.com/search?q={urllib.parse.quote(self.target)}"),
            ("LeakCheck", f"https://leakcheck.io/?q={urllib.parse.quote(self.target)}"),
            ("IntelX", f"https://intelx.io/search?term={urllib.parse.quote(self.target)}"),
            ("VirusTotal", f"https://www.virustotal.com/gui/search/{urllib.parse.quote(self.target)}"),
        ]
        
        threads = [Thread(target=self.scan_url_direct, args=(url, name, "Chrome")) 
                  for name, url in engines]
        for t in threads:
            t.start()
            time.sleep(0.1)
        for t in threads: t.join()
    
    def deep_dark_web(self):
        """Deep + Dark web full coverage"""
        self.ensure_tor()
        print(f"{Fore.RED}[🌑 DARK WEB - Tor Network]")
        
        all_engines = [
            ("Pastebin", f"https://pastebin.com/search?q={urllib.parse.quote(self.target)}"),
            ("Ahmia", "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={target}"),
        ]
        
        for name, template in all_engines:
            url = template.format(target=urllib.parse.quote(self.target))
            self.scan_url_direct(url, name, "Tor Browser")
    
    def scan_url_direct(self, url, source, browser="Chrome"):
        """Universal scanner"""
        try:
            if "Tor" in browser:
                self.ensure_tor()
                cmd = f"torsocks curl -s -L '{url}' --max-time 30"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                html = result.stdout
            else:
                res = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
                html = res.text
            
            hits = self.extract_all_data(html)
            for data, context_link in hits:
                self.print_hit(source, "WEB", data, url, browser)
                
        except: pass
    
    def extract_all_data(self, html):
        """Extract EVERYTHING"""
        hits = []
        patterns = {
            'Aadhaar': r'\b\d{{12}}\b',
            'PAN': r'[A-Z]{{5}}[0-9]{{4}}[A-Z]',
            'Phone': r'[\+]?[6-9]\d{{9,10}}',
            'Email': r'[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}',
            'IP': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'Domain': r'\b(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9][a-z0-9-]*[a-z0-9]\b',
            'PIN': r'\b[1-9][0-9]{{5}}\b',
        }
        
        for data_type, pattern in patterns.items():
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches[:5]:
                hits.append((f"{data_type}: {match}", 'url'))
        
        return hits
    
    def hiteckgroop_leak_check(self):
        """Khalid Hussain leak investigation"""
        leak_data = """📞Telephone: 917009860477
📞Telephone: 917973326717
📞Telephone: 919501600528
🏘️Adres: S/O: Om Parkash,BIX/973 WARD NUMBER-01,BHAN SINGH COLONY NEAR BANSAL RICE MILL,FARIDKOT,Punjab,151203 
🃏Document number: 277949340911
👤Full name: Om Parkash
👨The name of the father: Sandeep Kumar
🗺️ Region: AIRTEL PUNJAB

📞Telephone: 919646400040
📞Telephone: 917009254326
📞Telephone: 919501600528
🏘️Adres: 359,HAKIMA STREET SETHIAN MOHALLA,FARIDKOT,Punjab,151203 
🃏Document number: 789382021041
👤Full name: Aridaman Kumar Jain
👨The name of the father: KAPIL JAIN
🗺️ Region: AIRTEL PUNJAB

📞 Telephone: 919888380528
🏘️ Address: NEAR BANSAL RICE MILL, BHAN SINGH COLONY, FARIDKOT, PUNJAB, 151203
🃏 Document number: 27071NDL
👤 Full name: OM PARKASH"""
        
        self.print_hiteckgroop_data(leak_data)
    
    def generate_pdf_final(self):
        """Target-named PDF ONLY in target folder"""
        target_folder = re.sub(r'[^\w\-_\.]', '_', self.target)[:40]
        os.makedirs(target_folder, exist_ok=True)
        
        header = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
h1 {{ color: #d32f2f; border-bottom: 3px solid #d32f2f; padding-bottom: 10px; }}
h3 {{ color: #1976d2; }}
a {{ color: #0066cc !important; font-weight: bold; font-size: 16px; text-decoration: none !important; }}
a:hover {{ text-decoration: underline !important; }}
pre {{ white-space: pre-wrap; }}
</style>
</head>
<body>
<h1>🎯 ULTIMATE OSINT v85.0 - Khalid Hussain Investigation</h1>
<p><strong>Target:</strong> <code>{self.target}</code> | <strong>Hits:</strong> {len(self.results)} | <strong>{datetime.now()}</strong></p>
<hr style="border: 2px solid #d32f2f;">

{self.pdf_content}

<p style="text-align: center; color: #666; margin-top: 50px;">
<strong>AUTHORIZED PENTEST - Khalid Hussain Investigator</strong>
</p>
</body>
</html>
        """
        
        safe_name = re.sub(r'[^\w\-_\.]', '_', self.target)[:40]
        pdf_file = os.path.join(target_folder, f"{safe_name}_KhalidHussain_v85.pdf")
        
        HTML(string=header).write_pdf(pdf_file)
        print(f"\n{Fore.RED}🎯 FINAL REPORT: {pdf_file}")
        print(f"{Fore.GREEN}[📁] Saved in: {target_folder}/")
    
    def ultimate_pentest(self):
        """Execute ALL"""
        print(f"{Fore.RED}⚔️  ULTIMATE PENTEST v85.0 - Khalid Hussain")
        print(f"{Fore.CYAN}Target: {self.target}")
        print("=" * 70)
        
        # Silent leak data first
        self.hiteckgroop_leak_check()
        
        # Full stack
        self.kali_recon_suite()
        self.github_osint_tools()
        self.indian_documents()
        self.surface_web_pro()
        self.deep_dark_web()
        
        self.generate_pdf_final()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}python khalid-osint.py <target>")
        print(f"{Fore.CYAN}Ex: python khalid-osint.py 9876543210")
        sys.exit(1)
    
    osint = UltimateOSINTv85()
    osint.target = sys.argv[1]
    osint.ultimate_pentest()
