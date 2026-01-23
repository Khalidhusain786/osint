#!/usr/bin/env python3
"""
KHALID HUSAIN OSINT MASTER v4.0 - ALL TOOLS FIXED
"""

import os, sys, subprocess, requests, re, time, random, json, argparse
from colorama import Fore, Back, Style, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import signal

init(autoreset=True)
print_lock = Lock()

# ================================ REGEX PATTERNS ================================
SURE_HITS = {
    "🔥 PAN": r"[A-Z]{5}[0-9]{4}[A-Z]",
    "🆔 AADHAAR": r"\b\d{4}\s?\d{4}\s?\d{4}\b|\b\d{12}\b",
    "📖 PASSPORT": r"[A-Z][0-9]{7}|[A-Z]{2}\d{7}",
    "🏦 BANK": r"\b[0-9]{9,18}\b",
    "🗳️ VOTERID": r"[A-Z]{3}[0-9]{7}|[A-Z]{8}[0-9]{7}",
    "📱 PHONE": r"(?:\+91|0)?[6-9]\d{9}|\+\d{10,15}",
    "📍 PINCODE": r"\b\d{6}\b",
    "🚗 VEHICLE": r"[A-Z]{2}[0-9]{1,2}[A-Z]{0,2}[0-9]{4}",
    "🌐 IP": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "₿ BITCOIN": r"\b(?:1|3|bc1)[A-Za-z0-9]{25,62}\b",
    "💎 ETH": r"0x[a-fA-F0-9]{40}",
    "📧 EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "🏠 ADDRESS": r"(?i)(flat|house|plot|sector|gali|street|road|pin\s?\d{6})",
    "💳 CCARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b"
}

BANNER = f"""
{Fore.RED}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════╗
║{Fore.YELLOW}                    🧽 KHALID OSINT MASTER v4.0 🧽                     {Fore.RED}║
║{Fore.CYAN}    ALL-IN-ONE: Mariana/DarkWeb + Kali50+Tools + Social + SadLeaks    {Fore.RED}║
╠══════════════════════════════════════════════════════════════════════╣
║{Fore.GREEN}    sherlock•maigret•theHarvester•nmap•amass•subfinder•nikto...      {Fore.RED}║
║{Fore.MAGENTA}    PAN•Aadhaar•Phone•Bank•Email•BTC•DarkWeb•Social Profiles      {Fore.RED}║
╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

class KhalidOSINT:
    def __init__(self, target):
        self.target = target
        self.report_file = f"reports/KHALID_{target}_{int(time.time())}.txt"
        os.makedirs('reports', exist_ok=True)
        self.start_tor()
    
    def start_tor(self):
        os.system("sudo systemctl restart tor > /dev/null 2>&1")
        time.sleep(2)
        print(f"{Fore.GREEN}[🚀] TOR + Proxies ACTIVE")
    
    def get_headers(self):
        return {"User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
        ])}
    
    def get_tor_session(self):
        session = requests.Session()
        session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        retry_strategy = Retry(total=3, backoff_factor=1)
        session.mount('http://', HTTPAdapter(max_retries=retry_strategy))
        session.mount('https://', HTTPAdapter(max_retries=retry_strategy))
        return session
    
    def extract_sad_leaks(self, text, source="UNKNOWN"):
        """Extract SAD leaks - FIXED SYNTAX"""
        hits = {}
        for emoji_name, pattern in SURE_HITS.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                unique = list(set(matches))[:5]
                hits[emoji_name] = unique
        
        if hits:
            print(f"{Fore.RED}[{source}] 🎯 {len(hits)} LEAKS!")
            for name, values in hits.items():
                print(f"   {name}: {', '.join(values)}")
            
            with open(self.report_file, "a", encoding='utf-8') as f:
                f.write(f"\n🔥 [{source}-{time.strftime('%H:%M:%S')}] {len(hits)} HITS 🔥\n")
                for name, values in hits.items():
                    f.write(f"{name}: {', '.join(values)}\n")
    
    def mariana_dark_scan(self):
        print(f"{Fore.MAGENTA}[🌑 MARIANA] Scanning...")
        try:
            tor_session = self.get_tor_session()
            urls = [
                f"http://jnv3gv3yuvpwhv7y.onion/search/?q={self.target}",
                f"https://ahmia.fi/search/?q={self.target}"
            ]
            for url in urls:
                res = tor_session.get(url, timeout=20)
                self.extract_sad_leaks(res.text, "MARIANA")
        except: pass
    
    def social_blast(self):
        print(f"{Fore.CYAN}[📱 SOCIAL] Scanning...")
        social_urls = [
            f"https://www.google.com/search?q=%22{self.target}%22+site:facebook.com",
            f"https://www.google.com/search?q=%22{self.target}%22+site:instagram.com",
            f"https://www.google.com/search?q=%22{self.target}%22+site:twitter.com"
        ]
        for url in social_urls:
            try:
                res = requests.get(url, headers=self.get_headers(), timeout=10)
                self.extract_sad_leaks(res.text, "SOCIAL")
            except: pass
    
    def leak_databases(self):
        print(f"{Fore.RED}[💾 LEAKS] Hunting...")
        urls = [
            f"https://psbdmp.ws/api/search/{self.target}",
            f"https://www.google.com/search?q=%22{self.target}%22+filetype:sql"
        ]
        for url in urls:
            try:
                res = requests.get(url, headers=self.get_headers(), timeout=10)
                self.extract_sad_leaks(res.text, "LEAKS")
            except: pass
    
    def run_kali_tools(self):
        print(f"{Fore.GREEN}[⚔️ KALI] Arsenal...")
        kali_cmds = [
            ("SHERLOCK", f"sherlock {self.target} --timeout 10"),
            ("HOLEHE", f"holehe {self.target}"),
            ("HARVEST", f"theHarvester -d {self.target} -b google")
        ]
        
        for name, cmd in kali_cmds:
            try:
                print(f"  [KALI] Running {name}...")
                result = subprocess.run(f"timeout 30 {cmd}", shell=True, 
                                      capture_output=True, text=True)
                if result.stdout and self.target.lower() in result.stdout.lower():
                    print(f"  [{name}] HIT: {result.stdout[:100]}")
            except: pass
    
    def run_full_attack(self):
        print(f"{Fore.BLUE}🎯 TARGET: {self.target}")
        print(f"📄 REPORT: {self.report_file}\n")
        
        # All scanners
        self.mariana_dark_scan()
        self.social_blast()
        self.leak_databases()
        self.run_kali_tools()
        
        print(f"\n{Fore.GREEN}🎉 FULL SCAN COMPLETE!")
        print(f"📊 REPORT SAVED: {self.report_file}")

def main():
    parser = argparse.ArgumentParser(description='Khalid OSINT v4.0')
    parser.add_argument('target', help='Target name/email/phone/domain')
    args = parser.parse_args()
    
    print(BANNER)
    osint = KhalidOSINT(args.target)
    osint.run_full_attack()

if __name__ == "__main__":
    main()
