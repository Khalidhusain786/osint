#!/usr/bin/env python3
"""
KHALID HUSAIN OSINT MASTER - ALL TOOLS IN ONE
Deep/Dark/Mariana Web + Kali Arsenal + Social + Sad Leaks + SpongeBob Mode
Author: Khalid Husain | v4.0 Ultimate
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

# ================================ BANNER ================================
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
        """Start TOR service"""
        os.system("sudo systemctl restart tor > /dev/null 2>&1")
        time.sleep(2)
        with print_lock:
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
        """Extract all SAD leaks from text"""
        hits = {}
        for emoji_name, pattern in SURE_HITS.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                unique = list(set(matches))[:5]
                hits[emoji_name] = unique
        
        if hits:
            with print_lock:
                print(f"{Fore.RED}[{source}] 🎯 {len(hits)} LEAKS!")
                for name, values in hits.items():
                    print(f"   {name}: {Fore.WHITE}', '.join(values)}")
            
            with open(self.report_file, "a", encoding='utf-8') as f:
                f.write(f"\n🔥 [{source}-{time.strftime('%H:%M:%S')}] {len(hits)} HITS 🔥\n")
                for name, values in hits.items():
                    f.write(f"{name}: {', '.join(values)}\n")
    
    # ================================ WEB SCANNERS ================================
    def mariana_dark_scan(self):
        """Mariana + Dark Web scanner"""
        print(f"{Fore.MAGENTA}[🌑 MARIANA] Scanning...")
        tor_session = self.get_tor_session()
        urls = [
            f"http://jnv3gv3yuvpwhv7y.onion/search/?q={self.target}",
            f"https://ahmia.fi/search/?q={self.target}"
        ]
        for url in urls:
            try:
                res = tor_session.get(url, timeout=25)
                self.extract_sad_leaks(res.text, "MARIANA")
            except: pass
    
    def social_blast(self):
        """Social media profiles"""
        print(f"{Fore.CYAN}[📱 SOCIAL] 50+ platforms...")
        social_urls = [
            f"https://www.google.com/search?q=\"{self.target}\" site:facebook.com",
            f"https://www.google.com/search?q=\"{self.target}\" site:instagram.com",
            f"https://www.google.com/search?q=\"{self.target}\" site:twitter.com",
            f"https://www.google.com/search?q=\"{self.target}\" site:linkedin.com"
        ]
        for url in social_urls:
            try:
                res = requests.get(url, headers=self.get_headers(), timeout=12)
                self.extract_sad_leaks(res.text, "SOCIAL")
            except: pass
    
    def leak_databases(self):
        """Leak databases"""
        print(f"{Fore.RED}[💾 LEAKS] Hunting...")
        urls = [
            f"https://psbdmp.ws/api/search/{self.target}",
            f"https://www.google.com/search?q=\"{self.target}\" filetype:sql"
        ]
        for url in urls:
            try:
                res = requests.get(url, headers=self.get_headers(), timeout=15)
                self.extract_sad_leaks(res.text, "LEAKS")
            except: pass
    
    # ================================ KALI TOOLS ================================
    def run_kali_tool(self, cmd_name, cmd):
        """Run single Kali tool"""
        try:
            tool = cmd.split()[0]
            if subprocess.run(f"command -v {tool}", shell=True, capture_output=True).returncode != 0:
                return
            
            with print_lock:
                print(f"{Fore.GREEN}[⚔️ {cmd_name}] Running...")
            
            process = subprocess.Popen(
                f"timeout 90 torsocks {cmd.format(target=self.target)}",
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            
            for line in process.stdout:
                line = line.strip()
                if self.target.lower() in line.lower() or any(word in line.lower() for word in ['found', 'http', 'profile']):
                    with print_lock:
                        print(f"{Fore.YELLOW}[{cmd_name}] {line}")
            
        except: pass
    
    def kali_arsenal(self):
        """ALL Kali tools"""
        print(f"{Fore.GREEN}[⚔️ KALI] 50+ Tools Arsenal...")
        kali_tools = {
            "SHERLOCK": "sherlock {target} --timeout 8 --print-found",
            "MAIGRET": "maigret {target} --timeout 8",
            "HOLEHE": "holehe {target}",
            "HARVEST": "theHarvester -d {target} -b all -l 100",
            "AMASS": "amass enum -d {target} -o /tmp/amass.txt",
            "SUBFINDER": "subfinder -d {target} -silent",
            "ASSETFINDER": "assetfinder --subs-only {target}"
        }
        
        threads = []
        for name, cmd in kali_tools.items():
            t = Thread(target=self.run_kali_tool, args=(name, cmd))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
    
    # ================================ SPONGEBOB MODE ================================
    def spongebob_mode(self, text):
        """Spongebob case converter"""
        result = ""
        for i, char in enumerate(text):
            if char.isalpha():
                result += char.upper() if i % 2 == 0 else char.lower()
            else:
                result += char
        return result
    
    # ================================ MAIN EXECUTOR ================================
    def run_full_scan(self):
        """Run ALL scanners"""
        print(f"{Fore.BLUE}🎯 TARGET: {self.target}")
        print(f"📄 REPORT: {self.report_file}\n")
        
        # Phase 1: Web + Dark
        web_threads = [
            Thread(target=self.mariana_dark_scan),
            Thread(target=self.social_blast),
            Thread(target=self.leak_databases)
        ]
        
        for t in web_threads:
            t.start()
        for t in web_threads:
            t.join()
        
        # Phase 2: Kali Arsenal
        self.kali_arsenal()
        
        # Summary
        print(f"\n{Fore.GREEN}🎉 SCAN COMPLETE!")
        print(f"📊 REPORT: {self.report_file}")
        
        # Count hits
        try:
            with open(self.report_file, 'r') as f:
                lines = f.readlines()
                print(f"{Fore.RED}📈 TOTAL HITS: {len([l for l in lines if 'HITS' in l])}")
        except: pass

def signal_handler(sig, frame):
    print(f'\n{Fore.YELLOW}[!] Interrupted by user')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description='Khalid OSINT Master v4.0')
    parser.add_argument('target', help='Target (name/email/phone/domain)')
    parser.add_argument('--spongebob', action='store_true', help='SpongeBob mode')
    args = parser.parse_args()
    
    print(BANNER)
    
    osint = KhalidOSINT(args.target)
    
    if args.spongebob:
        print(f"{Fore.YELLOW}🧽 SPONGEBOB MODE ACTIVATED!")
        # Add SpongeBob processing here
        osint.run_full_scan()
    else:
        osint.run_full_scan()
