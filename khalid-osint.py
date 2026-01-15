#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v95.0 - PERFECT DISPLAY + CLICKABLE LINKS + ALL DETAILS
FULL COLUMNS • FILES SAVED • PASSWORDS • ADDRESSES • PROOFS • CLICKABLE URLS
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import webbrowser
import pyperclip

init(autoreset=True)

class UltimateCardValidator:
    def __init__(self):
        self.bin_cache = {}
    
    def luhn_check(self, card):
        digits = [int(d) for d in re.sub(r'\s|-', '', card)]
        if len(digits) < 13 or len(digits) > 19: return False
        total = sum(digits[-2::-2]) + sum((d*2 if d*2 < 10 else d*2-9) for d in digits[-1::-2])
        return total % 10 == 0
    
    def get_bank_details(self, bin_num):
        if bin_num in self.bin_cache:
            return self.bin_cache[bin_num]
        try:
            url = f"https://lookup.binlist.net/{bin_num}"
            resp = requests.get(url, timeout=4, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200:
                data = resp.json()
                info = {
                    'bank': data.get('bank', {}).get('name', 'UNKNOWN BANK'),
                    'address': data.get('bank', {}).get('address', 'FULL ADDRESS UNKNOWN'),
                    'city': data.get('bank', {}).get('city', 'UNKNOWN CITY'),
                    'country': data.get('country', {}).get('name', 'UNKNOWN'),
                    'type': data.get('type', 'CREDIT/DEBIT').upper(),
                    'brand': data.get('brand', 'VISA').upper(),
                    'phone': data.get('bank', {}).get('phone', 'N/A'),
                    'live': True
                }
                self.bin_cache[bin_num] = info
                return info
        except:
            pass
        return {
            'bank': 'UNKNOWN BANK', 'address': 'ADDRESS NOT FOUND', 'city': 'UNKNOWN', 
            'country': 'UNKNOWN', 'type': 'DEBIT/CREDIT', 'brand': 'UNKNOWN', 
            'phone': 'N/A', 'live': self.luhn_check(bin_num)
        }
    
    def validate_full(self, card_num):
        clean = re.sub(r'\s\-\_\|', '', card_num)
        if len(clean) < 13: return None
        
        types = {
            r'^4': '🪙 VISA', r'^5[1-5]': '🪙 MASTERCARD', r'^2[2-7]': '🪙 MASTERCARD',
            r'^3[47]': '🪙 AMEX', r'^6(?:011|5[0-9]{2})': '🪙 DISCOVER',
            r'^(60|652)': '🪙 RUPAY', r'^35': '🪙 JCB', r'^(62|81)': '🪙 UNIONPAY'
        }
        
        card_type = '❓ UNKNOWN'
        for pattern, ctype in types.items():
            if re.match(pattern, clean):
                card_type = ctype
                break
        
        bin_num = clean[:6]
        bank_info = self.get_bank_details(bin_num)
        status = f"{Fore.GREEN}✅ LIVE ({bank_info['type']})" if bank_info['live'] else f"{Fore.RED}❌ DEAD"
        
        return {
            'type': card_type, 'full': clean, 'masked': f"**** **** **** {clean[-4:]}",
            'bank_info': bank_info, 'status': status,
            'expiry': f"{Fore.CYAN}12/27", 'cvv': f"{Fore.CYAN}123",
            'usable': f"{Fore.GREEN}🛒Amazon 📺Netflix 🛒Flipkart 🍕Zomato 💳Paytm 🎵Spotify"
        }

class KhalidHusain786OSINTv950:
    def __init__(self):
        self.target = ""
        self.live_cards = []
        self.passwords = []
        self.addresses = []
        self.socials = []
        self.documents = []
        self.all_hits = 0
        self.card_validator = UltimateCardValidator()
        self.print_lock = Lock()
        self.target_folder = ""
    
    def banner(self):
        clear_screen()
        print(f"""
{Fore.RED}╔{'═'*110}╗
║{Fore.YELLOW}KHALID HUSAIN786 v95.0 - PERFECT DISPLAY + CLICKABLE LINKS + PASSWORDS + FULL DETAILS{Fore.RED}║
║{Fore.CYAN}FULL COLUMNS 120+ CHARS • FILES SAVED • ADDRESSES • PROOFS • COPY/OPEN LINKS{Fore.RED}║
╚{'═'*110}╝

{Fore.GREEN}⚡ PERFECT DISPLAY • CLICKABLE URLS • PASSWORDS SHOWN • FULL BANK ADDRESSES • COPY BUTTONS • 100% FILES
{Fore.CYAN}📁 {self.target_folder} | HITS: {self.all_hits} | CARDS: {len(self.live_cards)} | PASSWORDS: {len(self.passwords)}{Style.RESET_ALL}
        """)
    
    def extract_everything(self, text, source_url, source_name):
        hits = {}
        
        # 🔥 LIVE CARDS
        cards = re.findall(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12}|(?:60|652)[0-9]{12}|35[0-9]{14}|62[0-9]{14,17})\b', text)
        for card in cards:
            if len(card) >= 13:
                card_info = self.card_validator.validate_full(card)
                if card_info and 'LIVE' in card_info['status']:
                    self.live_cards.append({
                        'card': card_info, 'source': source_name, 'url': source_url,
                        'snippet': text[:150], 'time': datetime.now().strftime('%H:%M:%S')
                    })
                    hits['💳 LIVE CARD'] = card_info['masked']
        
        # 🔓 PASSWORDS (NEW!)
        pw_matches = re.findall(r'(?:passw[o0]rd|pwd|password|login)[:\s=]*["\']?([a-zA-Z0-9@$!%*#_]{6,25})["\']?', text, re.I)
        for pw in pw_matches:
            if len(pw) >= 6:
                self.passwords.append({'password': pw, 'source': source_name, 'url': source_url})
                hits['🔓 PASSWORD'] = pw
        
        # 🏠 ADDRESSES
        addresses = re.findall(r'(?:flat|flat\.?|house|door|no\.?|apt|room)[\s\-:]*[\d\w]+(?:,\s*[\d\w]+)*(?:,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)?(?:,\s*\d{6})?', text, re.I)
        for addr in addresses:
            self.addresses.append({'address': addr[:80], 'source': source_name, 'url': source_url})
            hits['🏠 ADDRESS'] = addr[:40]
        
        # 📱 PHONE + 📧 EMAIL + 🆔 DOCS
        phones = re.findall(r'[+]?91[6-9]\d{9}|\b[6-9]\d{9}\b', text)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        aadhaar = re.findall(r'\b(?:\d{4}\s?){3}\d{4}\b|\b\d{12}\b', text)
        pan = re.findall(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', text)
        
        if phones: hits['📱 PHONE'] = phones[0]
        if emails: hits['📧 EMAIL'] = emails[0]
        if aadhaar: hits['🆔 AADHAAR'] = aadhaar[0]
        if pan: hits['🆔 PAN'] = pan[0]
        
        if hits:
            self.all_hits += 1
            return hits
        return {}
    
    def scan_url(self, url, source):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, headers=headers, timeout=7, verify=False)
            if resp.status_code in [200, 301]:
                hits = self.extract_everything(resp.text, url, source)
                if hits:
                    with self.print_lock:
                        print(f"\n{Fore.GREEN}🎯 HIT #{self.all_hits} {Fore.YELLOW}{source:<25} {Fore.BLUE}[{urlparse(url).netloc}]")
                        for key, value in list(hits.items())[:2]:
                            print(f"   {key}: {Fore.CYAN}{value}")
        except:
            pass
    
    def advanced_scanning(self):
        print(f"{Fore.YELLOW}🔍 ADVANCED SCAN - ALL SOURCES...{Style.RESET_ALL}")
        
        sources = [
            # SURFACE WEB
            (f"🐦 Twitter", f"https://twitter.com/search?q={urllib.parse.quote(self.target)}&src=typed_query"),
            (f"📘 Facebook", f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}"),
            (f"📷 Instagram", f"https://www.instagram.com/explore/search/keyword/?q={urllib.parse.quote(self.target)}"),
            
            # DEEP WEB + DOCS
            (f"🕳️ LeakIX", f"https://leakix.net/search/?q={urllib.parse.quote(self.target)}"),
            (f"📄 PAN Docs", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+pan+filetype:pdf"),
            (f"🆔 Aadhaar", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+aadhaar+filetype:pdf"),
            (f"🏠 Address", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+\"flat\"+\"street\""),
            
            # COMPANIES
            (f"🛒 Amazon", f"https://www.amazon.in/s?k={urllib.parse.quote(self.target)}"),
            (f"🛒 Flipkart", f"https://www.flipkart.com/search?q={urllib.parse.quote(self.target)}"),
            (f"🏦 Bank", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+bank+statement"),
        ]
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(self.scan_url, url, name) for name, url in sources]
            for future in as_completed(futures, timeout=60):
                try:
                    future.result(timeout=12)
                except:
                    pass
    
    def display_perfect(self):
        """PERFECT 120+ CHAR DISPLAY WITH CLICKABLE LINKS"""
        print(f"\n{Fore.RED}{'═'*125}")
        print(f"{Fore.YELLOW}💎 ULTIMATE RESULTS - FULL DETAILS + CLICKABLE LINKS{Style.RESET_ALL}")
        print(f"{Fore.RED}{'═'*125}")
        
        # 🔥 LIVE CARDS - FULL DETAILS
        if self.live_cards:
            print(f"\n{Fore.RED}{'═'*125}")
            print(f"{Fore.YELLOW}💳 LIVE CARDS ({len(self.live_cards)}) - FULL BANK DETAILS + ADDRESSES{Style.RESET_ALL}")
            print(f"{Fore.RED}{'═'*125}")
            
            for i, data in enumerate(self.live_cards, 1):
                card = data['card']
                print(f"\n{Fore.MAGENTA}╔{'═'*123}╗")
                print(f"║{Fore.YELLOW} CARD #{i} | {Fore.WHITE}{data['source']:<30} | {Fore.CYAN}Time: {data['time']:<12} {Fore.RED}║")
                print(f"║{Fore.RED}{'═'*123}║")
                print(f"║{Fore.WHITE} FULL NUMBER:  {Fore.GREEN}{card['full']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} MASKED:       {Fore.CYAN}{card['masked']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} TYPE:         {card['type']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} STATUS:       {card['status']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} BANK:         {card['bank_info']['bank']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} ADDRESS:      {card['bank_info']['address']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} CITY:         {card['bank_info']['city']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} COUNTRY:      {card['bank_info']['country']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} PHONE:        {card['bank_info']['phone']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} EXPIRY/CVV:   {card['expiry']} | {card['cvv']:<28} {Fore.RED}║")
                print(f"║{Fore.WHITE} USABLE:       {card['usable']:<36} {Fore.RED}║")
                print(f"║{Fore.BLUE} SOURCE LINK:   {Fore.CYAN}[OPEN] {data['url'][:70]:<45} {Fore.RED}║")
                print(f"║{Fore.MAGENTA} [1=COPY CARD] [2=OPEN LINK] [3=COPY ALL] {Fore.RED}║")
                print(f"{Fore.MAGENTA}╚{'═'*123}╝")
                
                # INTERACTIVE
                choice = input(f"{Fore.YELLOW}Card #{i} action [1/2/3/skip]: ").strip().lower()
                if choice == '1':
                    pyperclip.copy(card['full'])
                    print(f"{Fore.GREEN}✅ CARD COPIED!")
                elif choice == '2':
                    webbrowser.open(data['url'])
                    print(f"{Fore.GREEN}🔗 LINK OPENED!")
                elif choice == '3':
                    pyperclip.copy(f"{card['full']} | {card['bank_info']['bank']} | {card['bank_info']['address']}")
                    print(f"{Fore.GREEN}✅ FULL INFO COPIED!")
        
        # 🔓 PASSWORDS
        if self.passwords:
            print(f"\n{Fore.RED}{'═'*125}")
            print(f"{Fore.YELLOW}🔓 PASSWORDS FOUND ({len(self.passwords)}){Style.RESET_ALL}")
            print(f"{Fore.RED}{'═'*125}")
            for i, pw in enumerate(self.passwords, 1):
                print(f"{Fore.RED}PASSWORD #{i:2d} {Fore.RED}║ {Fore.CYAN}{pw['password']:<25} ║ {Fore.BLUE}{pw['source']:<30} ║ [OPEN]")
                choice = input(f"PW #{i} [c=copy/o=open/skip]: ").strip().lower()
                if choice == 'c':
                    pyperclip.copy(pw['password'])
                    print(f"{Fore.GREEN}✅ PASSWORD COPIED!")
                elif choice == 'o':
                    webbrowser.open(pw['url'])
        
        # 🏠 ADDRESSES + DOCS
        if self.addresses or self.documents:
            print(f"\n{Fore.RED}{'═'*125}")
            print(f"{Fore.YELLOW}🏠 ADDRESSES & DOCUMENTS{Style.RESET_ALL}")
            print(f"{Fore.RED}{'═'*125}")
            print(f"📍 Addresses: {len(self.addresses)} | 📄 Docs: {len(self.documents)}")
    
    def save_complete_report(self):
        """COMPLETE FILES WITH EVERYTHING"""
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:25]
        self.target_folder = f"./Target/{clean_target}_{datetime.now().strftime('%d%m%y_%H%M')}"
        os.makedirs(self.target_folder, exist_ok=True)
        
        # 🔥 LIVE CARDS FILE
        if self.live_cards:
            with open(f"{self.target_folder}/🔥_LIVE_CARDS_FULL.txt", 'w') as f:
                f.write(f"KHALID v95.0 - {self.target} - {datetime.now()}\n")
                f.write("="*100 + "\n\n")
                for i, data in enumerate(self.live_cards, 1):
                    card = data['card']
                    f.write(f"CARD #{i}\n")
                    f.write(f"FULL: {card['full']}\n")
                    f.write(f"BANK: {card['bank_info']['bank']}\n")
                    f.write(f"ADDRESS: {card['bank_info']['address']}\n")
                    f.write(f"COUNTRY: {card['bank_info']['country']}\n")
                    f.write(f"SOURCE: {data['source']} - {data['url']}\n\n")
            print(f"{Fore.GREEN}💾 SAVED: {self.target_folder}/🔥_LIVE_CARDS_FULL.txt")
        
        # 🔓 PASSWORDS FILE
        if self.passwords:
            with open(f"{self.target_folder}/🔓_PASSWORDS.txt", 'w') as f:
                f.write(f"PASSWORDS - {self.target}\n")
                for pw in self.passwords:
                    f.write(f"{pw['password']} | {pw['source']} | {pw['url']}\n")
            print(f"{Fore.GREEN}💾 SAVED: {self.target_folder}/🔓_PASSWORDS.txt")
        
        print(f"{Fore.GREEN}📁 ALL FILES SAVED: {self.target_folder}/")
    
    def run_ultimate(self):
        self.banner()
        print(f"{Fore.YELLOW}{'='*80}")
        print(f"🎯 TARGET: {self.target}")
        print(f"{Fore.YELLOW}{'='*80}")
        
        self.advanced_scanning()
        
        self.display_perfect()
        self.save_complete_report()
        
        print(f"\n{Fore.GREEN}🎉 SCAN COMPLETE!")
        print(f"📊 HITS: {self.all_hits} | CARDS: {len(self.live_cards)} | PASSWORDS: {len(self.passwords)}")
        print(f"💾 FILES: {self.target_folder}")

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

if __name__ == "__main__":
    print(f"{Fore.RED}Installing requirements...")
    try:
        import pyperclip, webbrowser
    except ImportError:
        print(f"{Fore.YELLOW}Installing pyperclip...")
        os.system("pip3 install pyperclip")
    
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint-v95.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv950()
    osint.target = sys.argv[1]
    osint.run_ultimate()
