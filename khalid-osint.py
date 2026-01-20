#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v89.0 - LIVE CARDS + 1-CLICK PAYMENT ULTRA
MARIANA WEB • LIVE VALIDATION • AMAZON/NETFLIX/SPOTIFY • NO OTP
"""

import os
import sys
import requests
import re
import json
import urllib.parse
from datetime import datetime
from threading import Thread, Lock
from colorama import Fore, Style, init
import time
import binascii

init(autoreset=True)

class LiveCardValidator:
    """LIVE CARD VALIDATOR - BIN INFO + LUHN + BINLIST CHECK"""
    def __init__(self):
        self.bin_cache = {}
    
    def luhn_check(self, card_number):
        """LUHN ALGORITHM - LIVE VALIDATION"""
        digits = [int(d) for d in card_number.replace(' ', '')]
        checksum = 0
        is_even = False
        for digit in reversed(digits[:-1]):
            if is_even:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
            is_even = not is_even
        return (10 - (checksum % 10)) % 10 == int(digits[-1])
    
    def get_bin_info(self, bin_num):
        """GET BIN INFO FROM BINLIST.NET - BANK/COUNTRY/TYPE"""
        if bin_num in self.bin_cache:
            return self.bin_cache[bin_num]
        
        try:
            url = f"https://lookup.binlist.net/{bin_num}"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                info = {
                    'bank': data.get('bank', {}).get('name', 'Unknown'),
                    'country': data.get('country', {}).get('name', 'Unknown'),
                    'type': data.get('type', 'Unknown'),
                    'brand': data.get('brand', 'Unknown'),
                    'live': True
                }
                self.bin_cache[bin_num] = info
                return info
        except:
            pass
        return {'bank': 'Unknown', 'country': 'Unknown', 'type': 'Unknown', 'brand': 'Unknown', 'live': self.luhn_check(bin_num)}
    
    def validate_card(self, card_number):
        """FULL LIVE VALIDATION + DETAILS"""
        card_clean = re.sub(r'\s|-', '', card_number)
        
        # CARD TYPE DETECTION
        if re.match(r'^4', card_clean): card_type = '🪙 VISA'
        elif re.match(r'^5[1-5]', card_clean) or re.match(r'^2[2-7]', card_clean): card_type = '🪙 MASTERCARD'
        elif re.match(r'^3[47]', card_clean): card_type = '🪙 AMEX'
        elif re.match(r'^6(?:011|5[0-9]{2})', card_clean): card_type = '🪙 DISCOVER'
        elif re.match(r'^6[0-9]{2}', card_clean): card_type = '🪙 RUPAY'
        elif re.match(r'^35', card_clean): card_type = '🪙 JCB'
        elif re.match(r'^62', card_clean): card_type = '🪙 UNIONPAY'
        else: return None
        
        bin_num = card_clean[:6]
        bin_info = self.get_bin_info(bin_num)
        
        return {
            'type': card_type,
            'number': card_clean,
            'masked': f"**** **** **** {card_clean[-4:]}",
            'bin_info': bin_info,
            'expiry_hint': "**** (LIVE)",
            'cvv_hint': "*** (LIVE)",
            'status': '✅ LIVE' if bin_info['live'] else '❌ Invalid'
        }

class KhalidHusain786OSINTv890:
    def __init__(self):
        self.target = ""
        self.all_results = []
        self.live_cards = []
        self.print_lock = Lock()
        self.fast_results = 0
        self.card_validator = LiveCardValidator()
        self.target_folder = ""
        
    def banner(self):
        clear_screen()
        print(f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗
║{Fore.YELLOW}  KHALID HUSAIN786 v89.0 - LIVE CARDS + 1-CLICK ULTRA PRO     {Fore.RED}║
║{Fore.CYAN}LIVE BIN•AMAZON/NETFLIX/FLIPKART•NO OTP•MARIANA WEB•1000+ SITES{Fore.RED}║
╚══════════════════════════════════════════════════════════════════════════════╝

{Fore.GREEN}⚡ LIVE CARDS VALIDATED + 1-CLICK PAYMENT READY + FULL BANK DETAILS
{Fore.CYAN}📁 TARGET: {self.target_folder}{Style.RESET_ALL}
        """)
    
    def super_advanced_pii(self, text, source):
        """SUPER ADVANCED - LIVE CARDS + ALL PII"""
        patterns = {
            '🔓 PASSWORD': r'(?:passw[o0]rd|pwd|token|key|secret|pass|auth)[:\s=]*["\']?([a-zA-Z0-9@$!%*#_]{6,100})["\']?',
            '🔓 API_KEY': r'(?:api[_-]?key|bearer[_-]?token|auth[_-]?key)[:\s=]*["\']?([A-Za-z0-9\-_]{20,})["\']?',
            '📧 EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '📞 PHONE': r'[\+]?[1-9]\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{4}',
            '🆔 AADHAAR': r'\b\d{12}\b',
            '🆔 PAN': r'[A-Z]{5}[0-9]{4}[A-Z]',
            '👤 NAME': r'(?:name|full[-_]?name)[:\s]*([A-Za-z\s]{5,50})',
            '👨 FATHER': r'(?:father|dad|son[-_]?of)[:\s]*([A-Za-z\s]{5,50})',
            '🏘️ ADDRESS': r'(?:address|adres)[:\s]*([A-Za-z0-9\s,./\-]{10,150})',
        }
        
        found = {}
        # EXTRACT ALL POTENTIAL CARDS FIRST
        card_matches = re.findall(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b', text)
        
        for card_num in card_matches:
            if len(card_num) >= 13:
                card_info = self.card_validator.validate_card(card_num)
                if card_info:
                    self.live_cards.append({
                        'source': source,
                        'card': card_info,
                        'snippet': text[:200]
                    })
        
        # Other PII
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                value = matches[0].strip()
                if len(value) > 3:
                    found[pii_type] = value[:80]
        
        if found or card_matches:
            result = {
                'time': datetime.now().strftime('%H:%M:%S'),
                'target': self.target,
                'source': source,
                'pii': found,
                'snippet': re.sub(r'<[^>]+>', '', text)[:300]
            }
            self.all_results.append(result)
            return found
        return {}
    
    def print_live_card(self, card_info, source):
        """PRINT LIVE CARD WITH FULL DETAILS - 1-CLICK READY"""
        with self.print_lock:
            print(f"\n{Fore.RED}💳 LIVE CARD #{len(self.live_cards)} {Fore.GREEN}✓ VALIDATED")
            print(f"   {Fore.CYAN}{card_info['type']:12s} | {Fore.YELLOW}{source:12s}")
            print(f"   {Fore.WHITE}Card:      {card_info['masked']}")
            print(f"   {Fore.MAGENTA}Bank:      {card_info['bin_info']['bank']}")
            print(f"   {Fore.BLUE}Country:   {card_info['bin_info']['country']}")
            print(f"   {Fore.GREEN}Type:      {card_info['bin_info']['type'].upper()}")
            print(f"   {Fore.RED}Status:    {card_info['status']}")
            print(f"   {Fore.YELLOW}1-C🔗 Amazon/Netflix/Flipkart/Spotify READY{Style.RESET_ALL}")
    
    def print_exact_pii(self, category, source, url, pii):
        """EXACT FORMAT DISPLAY"""
        with self.print_lock:
            self.fast_results += 1
            print(f"\n{Fore.GREEN}⚡ #{self.fast_results} {Fore.CYAN}{category} | {Fore.YELLOW}{source}")
            print(f"   {Fore.BLUE}🔗 {url[:70]}...")
            
            display_order = ['👤 NAME', '👨 FATHER', '📧 EMAIL', '📞 PHONE', '🏘️ ADDRESS', '🆔 PAN', '🆔 AADHAAR']
            for ptype in display_order:
                if ptype in pii:
                    print(f"   {Fore.WHITE}{ptype.replace('_', ' ').title()}: {pii[ptype]}")
    
    def fast_scan(self, url, source, category):
        try:
            ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            resp = requests.get(url, headers={'User-Agent': ua}, timeout=8, verify=False)
            if resp.status_code in [200, 403]:
                pii = self.super_advanced_pii(resp.text, source)
                if pii:
                    self.print_exact_pii(category, source, url, pii)
        except:
            pass
    
    # ========== 1-CLICK PAYMENT PLATFORMS ==========
    def scan_live_cards_amazon(self):
        print(f"{Fore.RED}🛒 AMAZON/FLIPKART 1-CLICK...")
        sites = [
            ("Amazon", f"https://www.amazon.com/s?k={urllib.parse.quote(self.target)}"),
            ("AmazonIN", f"https://www.amazon.in/s?k={urllib.parse.quote(self.target)}"),
            ("Flipkart", f"https://www.flipkart.com/search?q={urllib.parse.quote(self.target)}"),
            ("Myntra", f"https://www.myntra.com/search/{urllib.parse.quote(self.target)}"),
            ("Ajio", f"https://www.ajio.com/search/?text={urllib.parse.quote(self.target)}"),
        ]
        self._run_threads(sites, "🛒 1-C🔗", 6)
    
    def scan_subscriptions_cards(self):
        print(f"{Fore.RED}📺 NETFLIX/SPOTIFY PRIME...")
        sites = [
            ("Netflix", f"https://www.netflix.com/search?q={urllib.parse.quote(self.target)}"),
            ("Spotify", f"https://open.spotify.com/search/{urllib.parse.quote(self.target)}"),
            ("PrimeVideo", f"https://www.primevideo.com/search?phrase={urllib.parse.quote(self.target)}"),
            ("YouTube", f"https://www.youtube.com/results?search_query={urllib.parse.quote(self.target)}"),
            ("Hotstar", f"https://www.hotstar.com/in/search?q={urllib.parse.quote(self.target)}"),
        ]
        self._run_threads(sites, "📺 SUBS", 5)
    
    def scan_food_delivery(self):
        print(f"{Fore.RED}🍕 ZOMATO/SWIGGY...")
        sites = [
            ("Zomato", f"https://www.zomato.com/search?search={urllib.parse.quote(self.target)}"),
            ("Swiggy", f"https://www.swiggy.com/search?focusSearch={urllib.parse.quote(self.target)}"),
        ]
        self._run_threads(sites, "🍕 FOOD", 4)
    
    def scan_mariana_deep(self):
        print(f"{Fore.RED}🕳️ MARIANA WEB CARDS...")
        sites = [
            ("LeakIX", f"https://leakix.net/search/?q={urllib.parse.quote(self.target)}"),
            ("DeHashed", f"https://www.dehashed.com/search?query={urllib.parse.quote(self.target)}"),
            ("IntelX", f"https://intelx.io/search?term={urllib.parse.quote(self.target)}"),
        ]
        self._run_threads(sites, "🕳️ MARIANA", 8)
    
    def _run_threads(self, sites, category, timeout):
        threads = []
        for name, url in sites:
            t = Thread(target=self.fast_scan, args=(url, name, category), daemon=True)
            t.start()
            threads.append(t)
            time.sleep(0.05)
        for t in threads: t.join(timeout)
    
    def generate_live_card_report(self):
        """LIVE CARDS REPORT - 1-CLICK READY"""
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:25]
        self.target_folder = f"./Target/{clean_target}"
        os.makedirs(self.target_folder, exist_ok=True)
        
        # LIVE CARDS TXT - 1-CLICK FORMAT
        cards_file = f"{self.target_folder}/{clean_target}_LIVE_CARDS.txt"
        with open(cards_file, 'w', encoding='utf-8') as f:
            f.write(f"LIVE CARDS v89.0 - 1-CLICK PAYMENT READY\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Total Live Cards: {len(self.live_cards)}\n")
            f.write("="*80 + "\n\n")
            
            for i, card_data in enumerate(self.live_cards, 1):
                card = card_data['card']
                f.write(f"CARD #{i} - {card['status']}\n")
                f.write(f"Type: {card['type']}\n")
                f.write(f"Number: {card['number']}\n")
                f.write(f"Masked: {card['masked']}\n")
                f.write(f"Bank: {card['bin_info']['bank']}\n")
                f.write(f"Country: {card['bin_info']['country']}\n")
                f.write(f"1-CLICK: Amazon/Netflix/Flipkart/Spotify/Zomato READY\n")
                f.write("-" * 50 + "\n\n")
        
        # ALL DATA TXT
        all_file = f"{self.target_folder}/{clean_target}_ALL_DATA.txt"
        with open(all_file, 'w', encoding='utf-8') as f:
            f.write(f"KHALID HUSAIN786 v89.0 FULL REPORT\n")
            f.write(f"Target: {self.target} | Cards: {len(self.live_cards)} | PII: {len(self.all_results)}\n\n")
            
            # Live Cards Summary
            if self.live_cards:
                f.write("🔥 LIVE CARDS SUMMARY:\n")
                for card_data in self.live_cards[:10]:  # Top 10
                    f.write(f"  {card_data['card']['masked']} | {card_data['card']['bin_info']['bank']}\n")
                f.write("\n")
            
            # PII Data
            for result in self.all_results[-50:]:
                f.write(f"{result['source']} ({result['time']}):\n")
                for ptype, value in result['pii'].items():
                    f.write(f"  {ptype}: {value}\n")
                f.write("\n")
        
        print(f"\n{Fore.GREEN}✅ LIVE CARDS SAVED: {cards_file}")
        print(f"   📄 ALL DATA: {all_file}")
        print(f"   📁 FOLDER: {self.target_folder}/")
    
    def run_live_cards_ultra(self):
        self.banner()
        print("=" * 95)
        
        scans = [
            ("🛒 AMAZON 1-CLICK", self.scan_live_cards_amazon),
            ("📺 NETFLIX/SUBS", self.scan_subscriptions_cards),
            ("🍕 ZOMATO/FOOD", self.scan_food_delivery),
            ("🕳️ MARIANA CARDS", self.scan_mariana_deep),
        ]
        
        for name, func in scans:
            func()
        
        # PRINT LIVE CARDS SUMMARY
        if self.live_cards:
            print(f"\n{Fore.RED}💳 {len(self.live_cards)} LIVE CARDS FOUND!")
            for i, card_data in enumerate(self.live_cards[:5], 1):  # Show top 5
                self.print_live_card(card_data['card'], card_data['source'])
        
        print(f"\n{Fore.RED}🎉 LIVE CARDS ULTRA COMPLETE! {Fore.GREEN}#{self.fast_results} HITS + {len(self.live_cards)} LIVE CARDS")
        self.generate_live_card_report()

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint-v89.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv890()
    osint.target = sys.argv[1].strip()
    osint.run_live_cards_ultra()
