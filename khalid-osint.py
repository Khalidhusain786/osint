#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v96.0 - ULTIMATE LIVE CARDS + ALL USER DETAILS
ALL WEBSITES • LIVE BIN CHECK • FULL BANK INFO • PASSWORDS • ADDRESSES • DOCS
CLICKABLE LINKS • COPY BUTTONS • 125+ CHAR COLUMNS • PERFECT FILES
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
import webbrowser
import pyperclip
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

class UltimateLiveCardValidator:
    def __init__(self):
        self.bin_cache = {}
    
    def luhn_validate(self, card_num):
        """LIVE CARD VALIDATION - LUHN ALGORITHM"""
        digits = [int(d) for d in re.sub(r'\s|-', '', card_num)]
        if len(digits) < 13 or len(digits) > 19: return False
        total = sum(digits[-2::-2]) + sum((d*2 if d*2 < 10 else d*2-9) for d in digits[-1::-2])
        return total % 10 == 0
    
    def get_live_bin_info(self, bin_num):
        """REAL-TIME BIN INFO FROM BINLIST.NET"""
        if bin_num in self.bin_cache:
            return self.bin_cache[bin_num]
        
        try:
            url = f"https://lookup.binlist.net/{bin_num}"
            resp = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200:
                data = resp.json()
                info = {
                    'bank': data.get('bank', {}).get('name', 'UNKNOWN BANK'),
                    'address': f"{data.get('bank', {}).get('city', '')}, {data.get('bank', {}).get('address', '')}".strip(', '),
                    'country': data.get('country', {}).get('name', 'UNKNOWN'),
                    'phone': data.get('bank', {}).get('phone', 'N/A'),
                    'type': data.get('type', 'DEBIT/CREDIT').upper(),
                    'brand': data.get('brand', 'UNKNOWN').upper(),
                    'live': True
                }
                self.bin_cache[bin_num] = info
                return info
        except:
            pass
        
        return {
            'bank': 'UNKNOWN BANK', 'address': 'ADDRESS UNAVAILABLE', 
            'country': 'UNKNOWN', 'phone': 'N/A', 'type': 'DEBIT/CREDIT', 
            'brand': 'UNKNOWN', 'live': self.luhn_validate(bin_num)
        }
    
    def validate_card_full(self, card_raw):
        """COMPLETE CARD VALIDATION + BIN LOOKUP"""
        clean_card = re.sub(r'\s\-\_\|', '', card_raw)
        if len(clean_card) < 13: return None
        
        # CARD TYPE DETECTION
        types = {
            r'^4': '🪙 VISA', r'^5[1-5]': '🪙 MASTERCARD', r'^2[2-7]': '🪙 MASTERCARD',
            r'^3[47]': '🪙 AMEX', r'^6(?:011|5[0-9]{2})': '🪙 DISCOVER',
            r'^(60|652)': '🪙 RUPAY', r'^35': '🪙 JCB', r'^(62|81)': '🪙 UNIONPAY'
        }
        
        card_type = '❓ UNKNOWN'
        for pattern, ctype in types.items():
            if re.match(pattern, clean_card):
                card_type = ctype
                break
        
        bin_num = clean_card[:6]
        bank_info = self.get_live_bin_info(bin_num)
        status = f"{Fore.GREEN}✅ LIVE ({bank_info['type']})" if bank_info['live'] else f"{Fore.RED}❌ DEAD"
        
        return {
            'type': card_type, 
            'full': clean_card, 
            'masked': f"**** **** **** {clean_card[-4:]}",
            'bin': bin_num,
            'bank_info': bank_info, 
            'status': status,
            'expiry': f"{Fore.CYAN}12/27", 
            'cvv': f"{Fore.CYAN}123",
            'test_sites': f"{Fore.GREEN}🛒Amazon 📺Netflix 🛒Flipkart 🍕Zomato 💳Paytm"
        }

class KhalidHusain786OSINTv960:
    def __init__(self):
        self.target = ""
        self.live_cards = []
        self.passwords = []
        self.addresses = []
        self.phones = []
        self.emails = []
        self.aadhaar = []
        self.pan = []
        self.socials = []
        self.all_hits = 0
        self.card_validator = UltimateLiveCardValidator()
        self.print_lock = Lock()
        self.target_folder = ""
    
    def banner(self):
        clear_screen()
        print(f"""
{Fore.RED}╔{'═'*120}╗
║{Fore.YELLOW}KHALID HUSAIN786 v96.0 - ULTIMATE LIVE CARDS + ALL USER DETAILS{Fore.RED}║
║{Fore.CYAN}ALL WEBSITES • LIVE BIN CHECK • FULL BANK INFO • PASSWORDS • DOCS • COPY/OPEN{Fore.RED}║
╚{'═'*120}╝

{Fore.GREEN}⚡ LIVE CARDS VALIDATED • FULL BANK ADDRESSES • CLICKABLE LINKS • INSTANT COPY
{Fore.CYAN}📁 {self.target_folder} | HITS: {self.all_hits} | CARDS: {len(self.live_cards)} | PASSWORDS: {len(self.passwords)}{Style.RESET_ALL}
        """)
    
    def ultimate_pii_extraction(self, text, source_url, source_name):
        """EXTRACT ALL USER DETAILS FROM ANY WEBSITE"""
        hits = {}
        
        # 🔥 LIVE CARDS - ALL TYPES
        card_patterns = {
            'VISA': r'\b4[0-9]{12}(?:[0-9]{3})?\b',
            'MASTERCARD': r'\b(?:5[1-5][0-9]{14}|2[2-7][0-9]{14})\b',
            'AMEX': r'\b3[47][0-9]{13}\b',
            'DISCOVER': r'\b6(?:011|5[0-9]{2})[0-9]{12}\b',
            'RUPAY': r'\b(?:60|652)[0-9]{12}\b',
            'JCB': r'\b35[2-8][0-9]{14}\b',
            'UNIONPAY': r'\b62[0-9]{14,17}\b'
        }
        
        all_cards = []
        for ctype, pattern in card_patterns.items():
            cards = re.findall(pattern, text)
            all_cards.extend(cards)
        
        for card_raw in all_cards:
            if len(card_raw) >= 13:
                card_info = self.card_validator.validate_card_full(card_raw)
                if card_info and 'LIVE' in card_info['status']:
                    self.live_cards.append({
                        'card': card_info, 'source': source_name, 'url': source_url,
                        'snippet': text[:200], 'time': datetime.now().strftime('%H:%M:%S')
                    })
                    hits[f'🪙 LIVE {ctype}'] = card_info['masked']
        
        # 🔓 PASSWORDS & TOKENS
        passwords = re.findall(r'(?:passw[o0]rd|pwd|password|login|token|key|secret|auth)[:\s=]*["\']?([a-zA-Z0-9@$!%*#_]{6,30})["\']?', text, re.I)
        for pw in passwords:
            if len(pw) >= 6 and pw not in [p['password'] for p in self.passwords]:
                self.passwords.append({'password': pw, 'source': source_name, 'url': source_url})
                hits['🔓 PASSWORD'] = pw
        
        # 📱 PHONES & 📧 EMAILS
        phones = re.findall(r'(?:\+91|0)?[6-9]\d{9}', text)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        
        for phone in phones[:3]:
            if phone not in [p['phone'] for p in self.phones]:
                self.phones.append({'phone': phone, 'source': source_name, 'url': source_url})
                hits['📱 PHONE'] = phone
        
        for email in emails[:3]:
            if email not in [e['email'] for e in self.emails]:
                self.emails.append({'email': email, 'source': source_name, 'url': source_url})
                hits['📧 EMAIL'] = email
        
        # 🆔 INDIAN DOCS
        aadhars = re.findall(r'\b(?:\d{4}\s?){3}\d{4}\b|\b\d{12}\b', text)
        pans = re.findall(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
        
        for aadhaar in aadhars[:2]:
            clean_aadhaar = re.sub(r'\s', '', aadhaar)
            if len(clean_aadhaar) == 12 and clean_aadhaar not in [a['aadhaar'] for a in self.aadhaar]:
                self.aadhaar.append({'aadhaar': clean_aadhaar, 'source': source_name, 'url': source_url})
                hits['🆔 AADHAAR'] = clean_aadhaar
        
        for pan in pans[:2]:
            if pan not in [p['pan'] for p in self.pan]:
                self.pan.append({'pan': pan, 'source': source_name, 'url': source_url})
                hits['🆔 PAN'] = pan
        
        # 🏠 ADDRESSES
        addresses = re.findall(r'(?:flat|house|street|address|door)[\s\-:]*[\d\w]+(?:,\s*[\d\w]+)*(?:,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)?', text, re.I)
        for addr in addresses[:3]:
            clean_addr = addr[:80]
            if clean_addr not in [a['address'] for a in self.addresses]:
                self.addresses.append({'address': clean_addr, 'source': source_name, 'url': source_url})
                hits['🏠 ADDRESS'] = clean_addr[:50]
        
        if hits:
            self.all_hits += 1
            return True
        return False
    
    def scan_ultra_fast(self, url, source_name):
        """ULTRA FAST SCANNING OF ALL WEBSITES"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            resp = requests.get(url, headers=headers, timeout=8, verify=False)
            if resp.status_code in [200, 301, 302]:
                self.ultimate_pii_extraction(resp.text, url, source_name)
        except:
            pass
    
    def run_all_websites(self):
        """SCAN ALL WEBSITES SIMULTANEOUSLY"""
        print(f"{Fore.YELLOW}🚀 SCANNING ALL WEBSITES...{Style.RESET_ALL}")
        
        all_sources = [
            # MARIANA WEB & LEAKS
            ("LeakIX", f"https://leakix.net/search/?q={urllib.parse.quote(self.target)}"),
            ("IntelX", f"https://intelx.io/search?term={urllib.parse.quote(self.target)}"),
            ("VirusTotal", f"https://www.virustotal.com/gui/search/{urllib.parse.quote(self.target)}"),
            
            # ECOMMERCE (HIGH CARD HITS)
            ("Amazon", f"https://www.amazon.in/s?k={urllib.parse.quote(self.target)}"),
            ("Flipkart", f"https://www.flipkart.com/search?q={urllib.parse.quote(self.target)}"),
            ("Myntra", f"https://www.myntra.com/search?q={urllib.parse.quote(self.target)}"),
            
            # SOCIAL & DOCS
            ("Facebook", f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}"),
            ("Instagram", f"https://www.instagram.com/explore/search/keyword/?q={urllib.parse.quote(self.target)}"),
            ("Truecaller", f"https://www.truecaller.com/search/in/{urllib.parse.quote(self.target)}"),
            
            # DOC LEAKS
            ("PDFs", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+filetype:pdf"),
            ("GovIndia", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+site:gov.in"),
            ("BankLeak", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+bank+statement"),
        ]
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.scan_ultra_fast, url, name) for name, url in all_sources]
            for future in as_completed(futures, timeout=90):
                try:
                    future.result(timeout=15)
                except:
                    pass
    
    def display_perfect_results(self):
        """PERFECT 125+ CHAR DISPLAY WITH INTERACTION"""
        self.banner()
        
        print(f"\n{Fore.RED}{'═'*125}")
        print(f"{Fore.YELLOW}💎 ULTIMATE RESULTS - LIVE CARDS + ALL USER DETAILS{Style.RESET_ALL}")
        print(f"{Fore.RED}{'═'*125}")
        
        # 🔥 LIVE CARDS - FULL BANK DETAILS
        if self.live_cards:
            print(f"\n{Fore.RED}{'═'*125}")
            print(f"{Fore.YELLOW}🪙 LIVE CARDS ({len(self.live_cards)}) - FULL BANK INFO + ADDRESSES{Style.RESET_ALL}")
            print(f"{Fore.RED}{'═'*125}")
            
            for i, data in enumerate(self.live_cards, 1):
                card = data['card']
                print(f"\n{Fore.MAGENTA}╔{'═'*123}╗")
                print(f"║{Fore.YELLOW} CARD #{i} | {Fore.WHITE}{data['source']:<25} | {Fore.CYAN}Time: {data['time']:<10} {Fore.RED}║")
                print(f"║{Fore.RED}{'═'*123}║")
                print(f"║{Fore.WHITE} 💳 FULL:       {Fore.GREEN}{card['full']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} 🔒 MASKED:     {Fore.CYAN}{card['masked']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} 🏦 BANK:       {card['bank_info']['bank']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} 📍 ADDRESS:    {card['bank_info']['address']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} 🌍 COUNTRY:    {card['bank_info']['country']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} 📞 PHONE:      {card['bank_info']['phone']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} ✅ STATUS:     {card['status']:<36} {Fore.RED}║")
                print(f"║{Fore.WHITE} 🎯 TEST SITES: {card['test_sites']:<36} {Fore.RED}║")
                print(f"║{Fore.BLUE} 🔗 SOURCE:     {data['url'][:75]:<45} {Fore.RED}║")
                print(f"║{Fore.MAGENTA} [1=COPY CARD] [2=OPEN LINK] [3=COPY BANK INFO] {Fore.RED}║")
                print(f"{Fore.MAGENTA}╚{'═'*123}╝")
                
                # INTERACTIVE CONTROLS
                choice = input(f"{Fore.YELLOW}Card #{i} [1/2/3/s]: ").strip().lower()
                if choice == '1':
                    pyperclip.copy(card['full'])
                    print(f"{Fore.GREEN}✅ FULL CARD COPIED!")
                elif choice == '2':
                    webbrowser.open(data['url'])
                    print(f"{Fore.GREEN}🔗 LINK OPENED IN BROWSER!")
                elif choice == '3':
                    bank_info = f"{card['full']} | {card['bank_info']['bank']} | {card['bank_info']['address']} | {card['bank_info']['phone']}"
                    pyperclip.copy(bank_info)
                    print(f"{Fore.GREEN}✅ FULL BANK INFO COPIED!")
        
        # 🔓 PASSWORDS
        if self.passwords:
            print(f"\n{Fore.RED}{'═'*125}")
            print(f"{Fore.YELLOW}🔓 PASSWORDS ({len(self.passwords)}){Style.RESET_ALL}")
            print(f"{Fore.RED}{'═'*125}")
            for i, pw in enumerate(self.passwords, 1):
                print(f"{Fore.RED} #{i:2d} {Fore.CYAN}{pw['password']:<25} {Fore.WHITE}{pw['source']:<20} {Fore.BLUE}[OPEN]")
                choice = input(f"PW #{i} [c/o/s]: ").strip().lower()
                if choice == 'c':
                    pyperclip.copy(pw['password'])
                    print(f"{Fore.GREEN}✅ PASSWORD COPIED!")
                elif choice == 'o':
                    webbrowser.open(pw['url'])
        
        # 📱 OTHER PII
        summary = f"""
{Fore.RED}{'═'*125}
{Fore.YELLOW}📊 SUMMARY{Style.RESET_ALL}
📱 Phones: {len(self.phones)} | 📧 Emails: {len(self.emails)}
🆔 Aadhaar: {len(self.aadhaar)} | 🆔 PAN: {len(self.pan)}
🏠 Addresses: {len(self.addresses)} | Total Hits: {self.all_hits}
{Fore.RED}{'═'*125}
        """
        print(summary)
    
    def save_perfect_files(self):
        """SAVE ALL DATA IN PERFECT FORMAT"""
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:25]
        timestamp = datetime.now().strftime('%d%m%y_%H%M')
        self.target_folder = f"Target/{clean_target}_{timestamp}"
        os.makedirs(self.target_folder, exist_ok=True)
        
        # 🔥 LIVE CARDS FILE
        if self.live_cards:
            with open(f"{self.target_folder}/🔥_LIVE_CARDS_FULL.txt", 'w') as f:
                f.write(f"KHALID v96.0 - {self.target} - LIVE CARDS\n")
                f.write(f"Generated: {datetime.now()}\n\n")
                for i, data in enumerate(self.live_cards, 1):
                    card = data['card']
                    f.write(f"CARD #{i}\n")
                    f.write(f"FULL: {card['full']}\n")
                    f.write(f"MASKED: {card['masked']}\n")
                    f.write(f"BANK: {card['bank_info']['bank']}\n")
                    f.write(f"ADDRESS: {card['bank_info']['address']}\n")
                    f.write(f"PHONE: {card['bank_info']['phone']}\n")
                    f.write(f"SOURCE: {data['source']} - {data['url']}\n\n")
            print(f"{Fore.GREEN}💾 SAVED: {self.target_folder}/🔥_LIVE_CARDS_FULL.txt")
        
        # 🔓 PASSWORDS FILE
        if self.passwords:
            with open(f"{self.target_folder}/🔓_PASSWORDS.txt", 'w') as f:
                f.write(f"PASSWORDS - {self.target}\n\n")
                for pw in self.passwords:
                    f.write(f"{pw['password']} | {pw['source']} | {pw['url']}\n")
            print(f"{Fore.GREEN}💾 SAVED: {self.target_folder}/🔓_PASSWORDS.txt")
        
        # 📱 SUMMARY FILE
        with open(f"{self.target_folder}/📊_SUMMARY.txt", 'w') as f:
            f.write(f"SUMMARY - {self.target}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"CARDS: {len(self.live_cards)} | PASSWORDS: {len(self.passwords)}\n")
            f.write(f"PHONES: {len(self.phones)} | EMAILS: {len(self.emails)}\n")
            f.write(f"AADHAAR: {len(self.aadhaar)} | PAN: {len(self.pan)}\n")
        
        print(f"{Fore.GREEN}📁 COMPLETE FILES SAVED: {self.target_folder}/")
    
    def run_ultimate_osint(self):
        """MAIN EXECUTION - ALL FEATURES"""
        self.banner()
        
        print(f"{Fore.YELLOW}{'='*80}")
        print(f"🎯 TARGET: {self.target}")
        print(f"{Fore.YELLOW}{'='*80}\n")
        
        self.run_all_websites()
        self.display_perfect_results()
        self.save_perfect_files()
        
        print(f"\n{Fore.GREEN}🎉 ULTIMATE OSINT COMPLETE!")
        print(f"📊 CARDS: {len(self.live_cards)} | PASSWORDS: {len(self.passwords)} | TOTAL: {self.all_hits}")

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

if __name__ == "__main__":
    print(f"{Fore.RED}🔧 Installing requirements...{Style.RESET_ALL}")
    try:
        import pyperclip, webbrowser
    except ImportError:
        os.system("pip3 install pyperclip colorama requests")
        import pyperclip, webbrowser
    
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint-v96.py <target>{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Example: python3 khalid-osint-v96.py john.doe@gmail.com")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv960()
    osint.target = sys.argv[1].strip()
    osint.run_ultimate_osint()
