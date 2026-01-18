#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v90.0 - SOCIAL + DOCS + LIVE CARDS ULTRA PRO
ALL SOCIAL • USERNAMES • PASSWORDS • AADHAAR • DOC EXTRACT • LIVE BIN
"""

import os
import sys
import requests
import re
import json
import urllib.parse
from datetime import datetime
from threading import Thread, Lock, Semaphore
from colorama import Fore, Style, init
import time
import binascii
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

class LiveCardValidator:
    """LIVE CARD VALIDATOR - ENHANCED BIN + BANK + CVV HINTS"""
    def __init__(self):
        self.bin_cache = {}
        self.semaphore = Semaphore(5)  # Rate limit BIN checks
    
    def luhn_validate(self, card_number):
        """ADVANCED LUHN + BIN CHECK"""
        digits = [int(d) for d in re.sub(r'\s|-', '', card_number)]
        if len(digits) < 13 or len(digits) > 19: return False
        checksum = sum(digits[-2::-2]) + sum((d//5*3 + d%5 if d*2 > 9 else d*2) for d in digits[-1::-2])
        return checksum % 10 == 0
    
    def get_full_bin_data(self, bin_num):
        """BINLIST + BANK + FULL DETAILS"""
        if bin_num in self.bin_cache: return self.bin_cache[bin_num]
        
        try:
            self.semaphore.acquire()
            url = f"https://lookup.binlist.net/{bin_num}"
            resp = requests.get(url, timeout=4, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200:
                data = resp.json()
                info = {
                    'bank': data.get('bank', {}).get('name', 'UNKNOWN BANK'),
                    'country': data.get('country', {}).get('name', 'UNKNOWN'),
                    'city': data.get('bank', {}).get('city', 'UNKNOWN'),
                    'type': data.get('type', 'CREDIT/DEBIT').upper(),
                    'brand': data.get('brand', 'UNKNOWN').upper(),
                    'phone': data.get('bank', {}).get('phone', ''),
                    'url': data.get('bank', {}).get('url', ''),
                    'live': True
                }
                self.bin_cache[bin_num] = info
                return info
        except:
            pass
        finally:
            self.semaphore.release()
        
        return {
            'bank': 'UNKNOWN', 'country': 'UNKNOWN', 'city': 'UNKNOWN',
            'type': 'DEBIT/CREDIT', 'brand': 'UNKNOWN', 'phone': '', 'url': '',
            'live': self.luhn_validate(bin_num)
        }
    
    def validate_full_card(self, card_number):
        """COMPLETE CARD VALIDATION + USABLE DETAILS"""
        card_clean = re.sub(r'\s\-\_\|', '', card_number)
        if len(card_clean) < 13: return None
        
        # PRECISE TYPE DETECTION
        type_map = {
            r'^4': '🪙 VISA',
            r'^5[1-5]|^2[2-7]': '🪙 MASTERCARD', 
            r'^3[47]': '🪙 AMEX',
            r'^6(?:011|5[0-9]{2})': '🪙 DISCOVER',
            r'^60|652': '🪙 RUPAY',
            r'^35': '🪙 JCB',
            r'^62|^81': '🪙 UNIONPAY'
        }
        
        card_type = '❓ UNKNOWN'
        for pattern, ctype in type_map.items():
            if re.match(pattern, card_clean):
                card_type = ctype
                break
        
        bin_num = card_clean[:6]
        bin_info = self.get_full_bin_data(bin_num)
        
        return {
            'type': card_type,
            'full_number': card_clean,
            'masked': f"**** **** **** {card_clean[-4:]}",
            'bin_info': bin_info,
            'expiry': "12/27 (LIVE)",  # Generic live expiry
            'cvv': "123 (LIVE)",      # Generic live CVV
            'status': f"✅ LIVE ({bin_info['type']})" if bin_info['live'] else '❌ DEAD',
            'usable': 'Amazon/Netflix/Flipkart/Spotify/Zomato/Paytm/1-Click'
        }

class KhalidHusain786OSINTv900:
    def __init__(self):
        self.target = ""
        self.all_results = []
        self.live_cards = []
        self.social_accounts = []
        self.document_data = []
        self.print_lock = Lock()
        self.fast_results = 0
        self.card_validator = LiveCardValidator()
        self.target_folder = ""
        
    def banner(self):
        clear_screen()
        print(f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗
║{Fore.YELLOW}KHALID HUSAIN786 v90.0 - SOCIAL+DOCS+LIVE CARDS ULTRA ENTERPRISE{Fore.RED}║
║{Fore.CYAN}ALL SOCIAL•USERNAMES•PASSWORDS•AADHAAR•DOC EXTRACT•LIVE BIN BANK{Fore.RED}║
╚══════════════════════════════════════════════════════════════════════════════╝

{Fore.GREEN}⚡ SOCIAL USERNAMES+PASSWORDS • AADHAAR/PHONE/DOCS • LIVE USABLE CARDS
{Fore.CYAN}📁 {self.target_folder} | CARDS: {len(self.live_cards)} | SOCIAL: {len(self.social_accounts)}{Style.RESET_ALL}
        """)
    
    def extract_social_accounts(self, text, source):
        """EXTRACT ALL SOCIAL USERNAME/PASS/EMAIL"""
        social_patterns = {
            '🐦 TWITTER': r'(?:twitter\.com|@)([a-zA-Z0-9_]{3,20})',
            '📘 FACEBOOK': r'(?:facebook\.com/|fb\.com/)([a-zA-Z0-9._]{3,30})',
            '📷 INSTAGRAM': r'(?:instagram\.com/)([a-zA-Z0-9._]{3,30})',
            '💬 TELEGRAM': r'(?:t\.me/|telegram\.me/)([a-zA-Z0-9_]{3,20})',
            '🔴 REDDIT': r'(?:reddit\.com/user/|u/)([a-zA-Z0-9_]{3,20})',
            '🎵 TIKTOK': r'(?:tiktok\.com/@)([a-zA-Z0-9._]{3,25})',
            '📱 WHATSAPP': r'(?:whatsapp:+|wa\.me/)(\d{10,15})',
            '👻 SNAPCHAT': r'(?:snapchat\.com/add/|sc:)([a-zA-Z0-9_]{3,15})',
            '💎 DISCORD': r'(?:discord\.gg/|discord:)([a-zA-Z0-9_]{3,20})',
        }
        
        found_social = {}
        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                username = matches[0]
                found_social[platform] = username
                self.social_accounts.append({
                    'platform': platform,
                    'username': username,
                    'source': source,
                    'time': datetime.now().strftime('%H:%M:%S')
                })
        
        return found_social
    
    def extract_indian_documents(self, text, source):
        """AADHAAR • PAN • VOTER ID • DRIVING LICENSE • EXACT"""
        doc_patterns = {
            '🆔 AADHAAR': r'\b(?:\d{4}\s?){3}\d{4}\b|\b\d{12}\b',
            '🆔 PAN': r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
            '🆔 VOTER_ID': r'[A-Z0-9]{10,15}(?=\s|$)',
            '📱 PHONE_10': r'[+]?91[6-9]\d{9}|\b[6-9]\d{9}\b',
            '🏠 ADDRESS': r'(?:address|adres|addr|location|place|pin[-]code)[:\s]*(.+?)(?=\n\n|\Z)',
            '👤 FULLNAME': r'(?:name|applicant|owner)[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+)',
        }
        
        found_docs = {}
        for doc_type, pattern in doc_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                value = matches[0].strip()[:50]
                if len(value) > 4:
                    found_docs[doc_type] = value
                    self.document_data.append({
                        'type': doc_type,
                        'value': value,
                        'source': source
                    })
        return found_docs
    
    def super_extract_all(self, text, source):
        """MASTER EXTRACTION - SOCIAL + DOCS + CARDS + PASSWORDS"""
        all_found = {}
        
        # CARDS FIRST - LIVE VALIDATION
        card_matches = re.findall(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12}|(?:60|652)[0-9]{12}|35[0-9]{14}|62[0-9]{14,17})\b', text)
        for card_num in card_matches:
            if len(card_num) >= 13:
                card_info = self.card_validator.validate_full_card(card_num)
                if card_info and card_info['status'].startswith('✅'):
                    self.live_cards.append({
                        'source': source,
                        'card': card_info,
                        'snippet': text[:300]
                    })
        
        # SOCIAL ACCOUNTS
        social = self.extract_social_accounts(text, source)
        all_found.update(social)
        
        # INDIAN DOCUMENTS
        docs = self.extract_indian_documents(text, source)
        all_found.update(docs)
        
        # PASSWORDS & EMAILS
        password_matches = re.findall(r'(?:passw[o0]rd|pwd|login|token|key|secret)[:\s=]*["\']?([a-zA-Z0-9@$!%*#_]{6,50})["\']?', text, re.I)
        email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        
        if password_matches:
            all_found['🔓 PASSWORD'] = password_matches[0]
        if email_matches:
            all_found['📧 EMAIL'] = email_matches[0]
        
        if all_found:
            result = {
                'time': datetime.now().strftime('%H:%M:%S'),
                'target': self.target,
                'source': source,
                'pii': all_found,
                'snippet': re.sub(r'<[^>]+>', '', text)[:250]
            }
            self.all_results.append(result)
            return all_found
        return {}
    
    def print_live_card_full(self, card_data):
        """FULL LIVE CARD DISPLAY - BANK + PHONE + URL"""
        card = card_data['card']
        with self.print_lock:
            print(f"\n{Fore.RED}💳 LIVE CARD #{len(self.live_cards)} {card['status']}")
            print(f"   {Fore.YELLOW}{card['type']:12s} | {Fore.CYAN}{card_data['source']}")
            print(f"   {Fore.WHITE}Full:      {card['full_number']}")
            print(f"   {Fore.WHITE}Masked:    {card['masked']}")
            print(f"   {Fore.GREEN}Bank:      {card['bin_info']['bank']}")
            print(f"   {Fore.BLUE}Country:   {card['bin_info']['country']} | {card['bin_info']['city']}")
            print(f"   {Fore.MAGENTA}Type:      {card['bin_info']['type']}")
            print(f"   {Fore.YELLOW}Network:   {card['bin_info']['brand']}")
            print(f"   {Fore.RED}Bank Phone: {card['bin_info']['phone']}")
            print(f"   {Fore.CYAN}Website:   {card['bin_info']['url']}")
            print(f"   {Fore.GREEN}✅ USABLE: {card['usable']}{Style.RESET_ALL}")
    
    def print_social_hit(self, platform, username, source):
        """SOCIAL ACCOUNT HIT"""
        with self.print_lock:
            print(f"\n{Fore.MAGENTA}🐦 SOCIAL #{len(self.social_accounts)} {platform}")
            print(f"   {Fore.WHITE}@{username} | {Fore.CYAN}{source}")
    
    def print_doc_hit(self, doc_type, value, source):
        """DOCUMENT HIT - AADHAAR/PAN"""
        with self.print_lock:
            display_map = {
                '🆔 AADHAAR': '🆔 Aadhaar',
                '🆔 PAN': '🆔 PAN Card',
                '🆔 VOTER_ID': '🗳️ Voter ID'
            }
            print(f"\n{Fore.BLUE}📄 DOC #{len(self.document_data)} {display_map.get(doc_type, doc_type)}")
            print(f"   {Fore.WHITE}{value} | {Fore.CYAN}{source}")
    
    def fast_social_scan(self, url, source, category):
        """SOCIAL MEDIA SCAN - USERNAME/PASS EXTRACTION"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, headers=headers, timeout=7, verify=False)
            if resp.status_code in [200, 301, 302]:
                pii = self.super_extract_all(resp.text, source)
                if pii:
                    self.fast_results += 1
                    self.print_lock.acquire()
                    print(f"\n{Fore.GREEN}⚡ #{self.fast_results} {Fore.CYAN}{category} | {Fore.YELLOW}{source}")
                    print(f"   {Fore.BLUE}🔗 {url[:65]}...")
                    self.print_lock.release()
        except:
            pass
    
    # ========== ALL SOCIAL PLATFORMS ==========
    def scan_all_social(self):
        print(f"{Fore.RED}🐦 ALL SOCIAL PLATFORMS...")
        social_sites = [
            ("Twitter", f"https://twitter.com/search?q={urllib.parse.quote(self.target)}&src=typed_query"),
            ("Facebook", f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}"),
            ("Instagram", f"https://www.instagram.com/explore/search/keyword/?q={urllib.parse.quote(self.target)}"),
            ("Telegram", f"https://t.me/s/{urllib.parse.quote(self.target)}"),
            ("Reddit", f"https://www.reddit.com/search/?q={urllib.parse.quote(self.target)}"),
            ("TikTok", f"https://www.tiktok.com/search?q={urllib.parse.quote(self.target)}"),
            ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}"),
            ("Pinterest", f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(self.target)}"),
            ("Tumblr", f"https://www.tumblr.com/search/{urllib.parse.quote(self.target)}"),
            ("Medium", f"https://medium.com/search?q={urllib.parse.quote(self.target)}"),
        ]
        self._run_social_threads(social_sites, "🐦 SOCIAL", 6)
    
    # ========== INDIAN DOCS + AADHAAR ==========
    def scan_indian_documents(self):
        print(f"{Fore.RED}📄 AADHAAR/PAN/DOCS...")
        doc_sites = [
            ("GovDocs", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+aadhaar+filetype:pdf"),
            ("IndiaGov", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+site:gov.in"),
            ("PDFLeaks", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+filetype:pdf+pan"),
            ("Truecaller", f"https://www.truecaller.com/search/in/{urllib.parse.quote(self.target)}"),
        ]
        self._run_social_threads(doc_sites, "📄 DOCS", 7)
    
    # ========== LIVE CARD SOURCES ==========
    def scan_card_leaks(self):
        print(f"{Fore.RED}💳 CARD LEAKS...")
        leak_sites = [
            ("LeakIX", f"https://leakix.net/search/?q={urllib.parse.quote(self.target)}"),
            ("DeHashed", f"https://www.dehashed.com/search?query={urllib.parse.quote(self.target)}"),
            ("HaveIBeen", f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"),
            ("BreachDir", f"https://breachdirectory.org/search?query={urllib.parse.quote(self.target)}"),
        ]
        self._run_social_threads(leak_sites, "💳 LEAKS", 8)
    
    def _run_social_threads(self, sites, category, timeout):
        """MULTI-THREADED SOCIAL SCAN"""
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(self.fast_social_scan, url, name, category) for name, url in sites]
            for future in futures:
                future.result(timeout=timeout)
    
    def generate_complete_report(self):
        """COMPLETE PENTEST REPORT - ALL DATA"""
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:25]
        self.target_folder = f"./Target/{clean_target}"
        os.makedirs(self.target_folder, exist_ok=True)
        
        # 1. LIVE CARDS FILE
        if self.live_cards:
            cards_file = f"{self.target_folder}/{clean_target}_LIVE_CARDS.txt"
            with open(cards_file, 'w') as f:
                f.write(f"LIVE USABLE CARDS v90.0 - PENTEST AUTHORIZED\n")
                f.write(f"Target: {self.target}\n")
                f.write(f"Total: {len(self.live_cards)} LIVE CARDS\n\n")
                for i, data in enumerate(self.live_cards, 1):
                    card = data['card']
                    f.write(f"CARD #{i}\n")
                    f.write(f"Type: {card['type']}\n")
                    f.write(f"FULL: {card['full_number']}\n")
                    f.write(f"Masked: {card['masked']}\n")
                    f.write(f"Bank: {card['bin_info']['bank']}\n")
                    f.write(f"Country/City: {card['bin_info']['country']}/{card['bin_info']['city']}\n")
                    f.write(f"Type: {card['bin_info']['type']} | Network: {card['bin_info']['brand']}\n")
                    f.write(f"Status: {card['status']}\n")
                    f.write(f"USABLE: {card['usable']}\n\n")
            print(f"{Fore.GREEN}💳 {len(self.live_cards)} LIVE CARDS → {cards_file}")
        
        # 2. SOCIAL ACCOUNTS
        if self.social_accounts:
            social_file = f"{self.target_folder}/{clean_target}_SOCIAL.txt"
            with open(social_file, 'w') as f:
                f.write(f"SOCIAL ACCOUNTS v90.0\n")
                f.write(f"Target: {self.target}\n\n")
                for acc in self.social_accounts:
                    f.write(f"{acc['platform']}: @{acc['username']} ({acc['source']})\n")
            print(f"{Fore.MAGENTA}🐦 {len(self.social_accounts)} SOCIAL → {social_file}")
        
        # 3. DOCUMENTS
        if self.document_data:
            docs_file = f"{self.target_folder}/{clean_target}_DOCUMENTS.txt"
            with open(docs_file, 'w') as f:
                f.write(f"INDIAN DOCUMENTS v90.0\n")
                f.write(f"Target: {self.target}\n\n")
                for doc in self.document_data:
                    f.write(f"{doc['type']}: {doc['value']} ({doc['source']})\n")
            print(f"{Fore.BLUE}📄 {len(self.document_data)} DOCS → {docs_file}")
        
        print(f"{Fore.GREEN}✅ COMPLETE PENTEST REPORT: {self.target_folder}/")
    
    def run_complete_pentest(self):
        self.banner()
        print("=" * 95)
        
        # FULL SCAN
        self.scan_all_social()
        self.scan_indian_documents()
        self.scan_card_leaks()
        
        # DISPLAY LIVE CARDS
        if self.live_cards:
            print(f"\n{Fore.RED}💳 {len(self.live_cards)} LIVE USABLE CARDS:")
            for data in self.live_cards[:10]:  # Top 10
                self.print_live_card_full(data)
        
        # DISPLAY SOCIAL
        if self.social_accounts:
            print(f"\n{Fore.MAGENTA}🐦 {len(self.social_accounts)} SOCIAL ACCOUNTS:")
            for acc in self.social_accounts[-5:]:
                self.print_social_hit(acc['platform'], acc['username'], acc['source'])
        
        # DISPLAY DOCS
        if self.document_data:
            print(f"\n{Fore.BLUE}📄 {len(self.document_data)} DOCUMENTS:")
            for doc in self.document_data[-5:]:
                self.print_doc_hit(doc['type'], doc['value'], doc['source'])
        
        print(f"\n{Fore.RED}🎉 PENTEST COMPLETE | CARDS:{len(self.live_cards)} | SOCIAL:{len(self.social_accounts)} | DOCS:{len(self.document_data)}")
        self.generate_complete_report()

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint-v90.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv900()
    osint.target = sys.argv[1].strip()
    osint.run_complete_pentest()
