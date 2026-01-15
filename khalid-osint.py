#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v89.2 - EXACT SCREEN FORMAT
"""

import os
import sys
import requests
import re
import time
from datetime import datetime
from threading import Thread, Lock
from colorama import Fore, Style, init

init(autoreset=True)

class KhalidHusain786OSINTv892:
    def __init__(self, target):
        self.target = target
        self.print_lock = Lock()
        self.hits = 0
        
    def banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗
║{Fore.YELLOW}         KHALID HUSAIN786 v89.2 - EXACT SCREEN FORMAT            {Fore.RED}║
║{Fore.CYAN}🔴 📞📞🏘️🃏👤👨🗺 - EXACT DISPLAY NO CHANGES{Fore.RED}║
╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """)
    
    def extract_exact_patterns(self, text):
        """🔥 EXACT PATTERNS FROM EXAMPLE"""
        data = {}
        
        # 📞Telephone - exact
        phones = re.findall(r'📞Telephone:\s*([\+91]?[6-9]\d{9,10})', text)
        data['📞Telephone'] = list(set(phones))
        
        # 🏘Adres / 🏘Address - exact
        addresses = re.findall(r'🏘(?:Adres|Address):\s*(.+?)(?=\n🏘|🃏|$)', text, re.DOTALL)
        data['🏘Adres'] = addresses
        
        # 🃏Document number
        docs = re.findall(r'🃏Document number:\s*(\d+)', text)
        data['🃏Document number'] = docs
        
        # 👤Full name
        names = re.findall(r'👤Full name:\s*([A-Za-z\s]+)', text)
        data['👤Full name'] = names
        
        # 👨Father's name / 👨The name of the father
        fathers = re.findall(r'👨(?:Father\'s name|The name of the father):\s*([A-Za-z\s]+)', text)
        data['👨Father\'s name'] = fathers
        
        # 🗺 Region
        regions = re.findall(r'🗺 Region:\s*(.+)', text)
        data['🗺 Region'] = regions
        
        # Other cards/numbers
        adhar = re.findall(r'Adhar card:\s*(\d+)', text)
        pan = re.findall(r'Pan card\s*:\s*(\d+)', text)
        master = re.findall(r'Master card\s*:\s*(\d+)', text)
        
        data['Adhar card'] = adhar
        data['Pan card'] = pan
        data['Master card'] = master
        
        return data
    
    def print_exact_format(self, data, source):
        """🔥 EXACT SCREEN FORMAT - NO CHANGES"""
        self.hits += 1
        
        print(f"\n{Fore.RED}Engine: {source} ... Google.com{Style.RESET_ALL}")
        
        # 📞Telephone
        if '📞Telephone' in data:
            for phone in data['📞Telephone'][:8]:
                print(f"  📞Telephone: {phone}")
        
        # Alternative number
        if 'Alternative number' in data:
            print(f"    Alternative number: {data['Alternative number'][0]}")
        
        # 🏘Adres
        if '🏘Adres' in data:
            for addr in data['🏘Adres'][:4]:
                print(f" 🏘Adres: {addr.strip()}")
        
        # 🃏Document number
        if '🃏Document number' in data:
            for doc in data['🃏Document number']:
                print(f" 🃏Document number: {doc}")
        
        # 👤Full name
        if '👤Full name' in data:
            for name in data['👤Full name']:
                print(f" 👤Full name: {name.strip()}")
        
        # 👨Father's name
        if '👨Father\'s name' in data:
            for father in data["👨Father's name"]:
                print(f" 👨The name of the father: {father.strip()}")
        
        # 🗺 Region
        if '🗺 Region' in data:
            for region in data['🗺 Region']:
                print(f" 🗺 Region: {region.strip()}")
        
        # Cards
        for card_type in ['Adhar card', 'Pan card', 'Master card']:
            if card_type in data:
                for num in data[card_type]:
                    print(f" {card_type}: {num}")
        
        print(" Email")
        print(" Password")
        print(f" IP")
        print(" social")
        print(" btc")
        print(" Father no")
        print(" Mother no")
    
    def scan_source(self, query, source_name):
        """🔥 Scan with exact query"""
        try:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                data = self.extract_exact_patterns(resp.text)
                if any(data.values()):
                    with self.print_lock:
                        self.print_exact_format(data, source_name)
        except:
            pass
    
    def run_exact_format(self):
        self.banner()
        print(f"{Fore.RED}{'='*100}{Style.RESET_ALL}")
        
        queries = [
            f"{self.target}",
            f"{self.target} telephone",
            f"{self.target} adres",
            f"{self.target} document number",
            f"{self.target} full name",
            f"{self.target} father",
            f"{self.target} punjab",
            f"{self.target} faridkot",
            f"{self.target} adhar",
            f"{self.target} pan card"
        ]
        
        print(f"{Fore.CYAN}🔥 Scanning {self.target} - EXACT FORMAT{Style.RESET_ALL}")
        
        threads = []
        for i, query in enumerate(queries):
            source_name = f"SOURCE{i+1}"
            t = Thread(target=self.scan_source, args=(query, source_name), daemon=True)
            t.start()
            threads.append(t)
            time.sleep(0.1)
        
        for t in threads:
            t.join()
        
        print(f"\n{Fore.RED}✅ EXACT FORMAT COMPLETE - {self.hits} HITS{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    target = sys.argv[1]
    osint = KhalidHusain786OSINTv892(target)
    osint.run_exact_format()
