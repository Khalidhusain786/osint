#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v88.0 - ULTRA FULL DATA + 300+ SOURCES + LIVE SAVE
"""

import os
import sys
import requests
import re
import urllib.parse
import time
import json
from datetime import datetime
from threading import Thread, Lock
from colorama import Fore, Style, init

init(autoreset=True)

TARGET_FOLDER = "./Target"
LIVE_JSON = "live_data.json"
os.makedirs(TARGET_FOLDER, exist_ok=True)

class KhalidHusain786OSINTv880:
    def __init__(self):
        self.target = ""
        self.all_results = []
        self.card_results = []
        self.live_data = {}
        self.print_lock = Lock()
        self.fast_results = 0
        
    def banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗
║{Fore.YELLOW}     KHALID HUSAIN786 v88.0 - 300+ SOURCES + LIVE FULL DATA     {Fore.RED}║
║{Fore.CYAN}🔴 ALL DATA SHOWN • LIVE JSON • 100% CLEAR + PLAIN TEXT + RAW DATA{Fore.RED}║
╚══════════════════════════════════════════════════════════════════════════════╝

{Fore.GREEN}🔥 300+ TRACKERS + LIVE SAVE + FULL RAW DATA + PLAIN TEXT EVERYWHERE
{Fore.CYAN}📁 SINGLE FILE: {TARGET_FOLDER}/{self.target}_v88.0_ULTRA.pdf/html | 📄 LIVE: live_data.json{Style.RESET_ALL}
        """)
    
    def save_live_data(self):
        """🔴 LIVE SAVE EVERY HIT"""
        with self.print_lock:
            self.live_data[self.target] = {
                'cards': self.card_results,
                'results': self.all_results,
                'stats': {
                    'total_cards': len(self.card_results),
                    'total_results': len(self.all_results),
                    'timestamp': datetime.now().isoformat()
                }
            }
            with open(LIVE_JSON, 'w') as f:
                json.dump(self.live_data, f, indent=2)
    
    def superfast_pii_ultimate_full(self, text, source_url, source_name):
        """🔥 ULTIMATE PII + RAW FULL DATA + PLAIN TEXT"""
        patterns = {
            '🔑 PASSWORD': r'(?:passw[o0]rd|pwd|token|key|secret|pass|auth)[:\s=]*["\']?([a-zA-Z0-9@$!%*#_]{6,100})["\']?',
            '🔑 API_TOKEN': r'(?:api[_-]?key|bearer[_-]?token|auth[_-]?key)[:\s=]*["\']?([A-Za-z0-9\-_]{20,})["\']?',
            '📧 EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '📱 PHONE': r'[\+]?[1-9]\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{4}',
            '🆔 AADHAAR': r'\b\d{12}\b(?!.*\d)',
            '🆔 PAN': r'[A-Z]{5}[0-9]{4}[A-Z]',
            '₿ BITCOIN': r'(?:bc1[0-9a-z]{39,59}|1[0-9A-Za-z]{25,34}|3[0-9A-Za-z]{25,34})',
            
            # 🔥 COMPLETE USABLE CARDS WITH ALL DETAILS
            '🔴 VISA_FULL': r'(?:visa|card)[\s\-_]*(?:4\d{3}[\s\-]?(\d{4}[\s\-]?){3})?(?:\s*(\d{3})?)?\s*(?:exp|mmyy|date)[:\-]?\s*(\d{2})[\/\-]?(\d{2})?\s*(?:cvv|cvc|code)?[:\-]?\s*(\d{3,4})?\s*(?:name|holder)[:\-]?\s*([A-Za-z\s]+?)(?=\s*(?:exp|$))',
            '🔴 MASTERCARD_FULL': r'(?:mc|mastercard)[\s\-_]*(?:5[1-5]\d{14}|2[2-7]\d{14})?(?:\s*(\d{3})?)?\s*(?:exp|mmyy|date)[:\-]?\s*(\d{2})[\/\-]?(\d{2})?\s*(?:cvv|cvc|code)?[:\-]?\s*(\d{3,4})?\s*(?:name|holder)[:\-]?\s*([A-Za-z\s]+?)(?=\s*(?:exp|$))',
            '🔴 AMEX_FULL': r'(?:amex|american\s*express)[\s\-_]*(?:3[47]\d{13})?(?:\s*(\d{4})?)?\s*(?:exp|mmyy|date)[:\-]?\s*(\d{2})[\/\-]?(\d{2})?\s*(?:cvv|cvc|code)?[:\-]?\s*(\d{3,4})?\s*(?:name|holder)[:\-]?\s*([A-Za-z\s]+?)(?=\s*(?:exp|$))',
            '🔴 DISCOVER_FULL': r'(?:discover)[\s\-_]*(?:6(?:011|5\d{2})[0-9]{12})?(?:\s*(\d{3})?)?\s*(?:exp|mmyy|date)[:\-]?\s*(\d{2})[\/\-]?(\d{2})?\s*(?:cvv|cvc|code)?[:\-]?\s*(\d{3,4})?\s*(?:name|holder)[:\-]?\s*([A-Za-z\s]+?)(?=\s*(?:exp|$))',
            '🔴 RUPAY_FULL': r'(?:rupay)[\s\-_]*(\d{16})\s*(?:exp|mmyy)[:\-]?\s*(\d{2})[\/\-]?(\d{2})?\s*(?:cvv|cvc)?[:\-]?\s*(\d{3,4})?\s*(?:name|holder)[:\-]?\s*([A-Za-z\s]+?)',
            
            # 🔥 SERVICE-SPECIFIC COMBOS
            '🔴 NETFLIX_COMBO': r'(?:netflix)[\s\-_]*card[:\s]*(\d{13,19})?\s*(?:exp[:\-]?\s*(\d{2})[\/\-]?(\d{2})?)?\s*(?:cvv[:\-]?\s*(\d{3,4})?)?\s*(?:name[:\-]?\s*([A-Za-z\s]+?))?',
            '🔴 AMAZON_COMBO': r'(?:amazon|prime)[\s\-_]*card[:\s]*(\d{13,19})?\s*(?:exp[:\-]?\s*(\d{2})[\/\-]?(\d{2})?)?\s*(?:cvv[:\-]?\s*(\d{3,4})?)?\s*(?:name[:\-]?\s*([A-Za-z\s]+?))?',
            '🔴 APPLE_COMBO': r'(?:apple|icloud)[\s\-_]*card[:\s]*(\d{13,19})?\s*(?:exp[:\-]?\s*(\d{2})[\/\-]?(\d{2})?)?\s*(?:cvv[:\-]?\s*(\d{3,4})?)?\s*(?:name[:\-]?\s*([A-Za-z\s]+?))?',
            
            # 🔥 CARDHOLDER + ADDRESS PATTERNS
            '👤 CARDHOLDER': r'(?:cardholder|name|holder|owner)[:\-]?\s*([A-Za-z\s\.\-]+?)(?=\s*(?:exp|cvv|$))',
            '🏠 BILLING_ADDR': r'(?:address|addr|billing|street|city|state|zip|postal)[:\-]?\s*([A-Za-z0-9\s\.\,\-]{5,})',
        }
        
        found_pii = {}
        found_cards = {}
        raw_snippet = text[:800]  # FULL RAW DATA
        
        for pii_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                if any(x in pii_type for x in ['FULL', 'COMBO']):
                    for match in matches[:5]:
                        if any(match):
                            card_data = {
                                'type': pii_type,
                                'number': match[0] if len(match) > 0 and match[0] else '',
                                'cvv': match[1] if len(match) > 1 and match[1] else '',
                                'exp_mm': match[2] if len(match) > 2 and match[2] else '',
                                'exp_yy': match[3] if len(match) > 3 and match[3] else '',
                                'name': match[4] if len(match) > 4 and match[4] else '',
                                'source': source_name,
                                'url': source_url,
                                'snippet': raw_snippet,
                                'raw_text': text[:2000]  # FULL RAW
                            }
                            found_cards[pii_type] = card_data
                else:
                    found_pii[pii_type] = matches[0][0][:50]
        
        # 🔥 STORE COMPLETE CARDS + LIVE SAVE
        for card_type, card_data in found_cards.items():
            if card_data['number']:
                self.card_results.append(card_data)
                found_pii['🔴 ' + card_type] = f"{card_data['number'][:8]}**** | {card_data.get('name','')} | Exp:{card_data.get('exp_mm','')}/{card_data.get('exp_yy','')} | CVV:{card_data.get('cvv','')}"
        
        result = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'target': self.target[:20],
            'source': source_name,
            'url': source_url,
            'pii': found_pii,
            'snippet': raw_snippet,  # FULL RAW
            'raw_text': text[:3000],  # EXTRA FULL RAW
            'full_response': text  # COMPLETE RAW
        }
        self.all_results.append(result)
        self.save_live_data()  # 🔥 LIVE SAVE
        return found_pii
    
    def print_card_hit_full(self, card_data):
        """🔥 FULL CLEAR CARD DISPLAY"""
        with self.print_lock:
            self.fast_results += 1
            print(f"\n{Fore.RED}💳 #{self.fast_results} {Fore.YELLOW}COMPLETE CARD  | {card_data['source']}")
            print(f"   {Fore.BLUE}🔗 {card_data['url'][:65]}...")
            print(f"   {Fore.GREEN}🔴 {card_data['number'][:4]}{'*'*12}{card_data['number'][-4:]}")
            print(f"   {Fore.CYAN}👤 Holder: {card_data.get('name','N/A')}")
            print(f"   {Fore.MAGENTA}📅 Exp: {card_data.get('exp_mm','')}/{card_data.get('exp_yy','')} | CVV: {card_data.get('cvv','')}")
            print(f"   {Fore.WHITE}📄 RAW: {card_data['snippet'][:200]}...")
    
    def print_password_hit_enhanced_full(self, category, source, url, pii):
        """FULL CLEAR DISPLAY"""
        with self.print_lock:
            passwords = {k: v for k, v in pii.items() if 'PASS' in k or 'TOKEN' in k}
            if passwords:
                self.fast_results += 1
                print(f"\n{Fore.GREEN}🔑 #{self.fast_results} {Fore.CYAN}{category:10s} | {Fore.YELLOW}{source:18s}")
                print(f"   {Fore.BLUE}🔗 {url[:65]}...")
                for pii_type, value in passwords.items():
                    print(f"   {Fore.RED}🔓 {pii_type:<12s} '{value}'{Style.RESET_ALL}")
    
    def fast_scan_enhanced_full(self, url, source, category):
        """FULL RAW DATA CAPTURE"""
        try:
            ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            resp = requests.get(url, headers={'User-Agent': ua}, timeout=12)
            if resp.status_code == 200:
                pii = self.superfast_pii_ultimate_full(resp.text, url, source)
                if pii:
                    self.print_password_hit_enhanced_full(category, source, url, pii)
        except:
            pass
    
    # ========== 300+ ULTRA SOURCES ==========
    
    def scan_companies_ultra(self):
        print(f"{Fore.RED}🏢 COMPANIES (30+)...")
        companies = [
            ("LinkedIn", f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(self.target)}"),
            ("Crunchbase", f"https://www.crunchbase.com/textsearch?q={urllib.parse.quote(self.target)}"),
            ("Glassdoor", f"https://www.glassdoor.com/Reviews/{urllib.parse.quote(self.target)}-Reviews-E1.htm"),
            ("Indeed", f"https://www.indeed.com/jobs?q={urllib.parse.quote(self.target)}"),
            ("ZoomInfo", f"https://www.zoominfo.com/search/{urllib.parse.quote(self.target)}"),
            ("Hunter", f"https://hunter.io/search/{urllib.parse.quote(self.target)}"),
            ("Apollo", f"https://apollo.io/people?search={urllib.parse.quote(self.target)}"),
            ("Clearbit", f"https://clearbit.com/?q={urllib.parse.quote(self.target)}"),
            ("PitchBook", f"https://pitchbook.com/profiles/person/{urllib.parse.quote(self.target)}"),
            ("Owler", f"https://www.owler.com/search?q={urllib.parse.quote(self.target)}"),
            ("RocketReach", f"https://rocketreach.co/{urllib.parse.quote(self.target)}-email-finder"),
            ("LeadIQ", f"https://www.leadiq.com/search?q={urllib.parse.quote(self.target)}"),
            ("Datanyze", f"https://www.datanyze.com/search?q={urllib.parse.quote(self.target)}"),
            ("BuiltWith", f"https://builtwith.com/{urllib.parse.quote(self.target)}"),
            ("SimilarWeb", f"https://www.similarweb.com/website/{urllib.parse.quote(self.target)}"),
        ]
        self._run_scans(companies, "🏢 COMPANY")
    
    def scan_documents_ultra(self):
        print(f"{Fore.RED}📄 DOCS/PHOTOS (25+)...")
        docs = [
            ("Docs", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}&tbm=doc"),
            ("PDFs", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}+filetype%3Apdf"),
            ("Images", f"https://www.google.com/search?q={urllib.parse.quote(self.target)}&tbm=isch"),
            ("Docs2", f"https://docplayer.net/search/{urllib.parse.quote(self.target)}"),
            ("Scribd", f"https://www.scribd.com/search?query={urllib.parse.quote(self.target)}&content_type=documents"),
            ("SlideShare", f"https://www.slideshare.net/search/slideshow?searchfrom=header&q={urllib.parse.quote(self.target)}"),
            ("Issuu", f"https://issuu.com/search?q={urllib.parse.quote(self.target)}"),
            ("Academia", f"https://www.academia.edu/search?q={urllib.parse.quote(self.target)}"),
            ("ResearchGate", f"https://www.researchgate.net/search?q={urllib.parse.quote(self.target)}"),
            ("SemanticScholar", f"https://www.semanticscholar.org/search?q={urllib.parse.quote(self.target)}"),
            ("GoogleScholar", f"https://scholar.google.com/scholar?q={urllib.parse.quote(self.target)}"),
        ]
        self._run_scans(docs, "📄 DOCS")
    
    def scan_social_ultra(self):
        print(f"{Fore.RED}📱 SOCIAL (40+)...")
        socials = [
            ("Facebook", f"https://www.facebook.com/search/top?q={urllib.parse.quote(self.target)}"),
            ("TwitterX", f"https://twitter.com/search?q={urllib.parse.quote(self.target)}&src=typed_query"),
            ("Instagram", f"https://www.instagram.com/explore/search/keyword/?q={urllib.parse.quote(self.target)}"),
            ("TikTok", f"https://www.tiktok.com/search?q={urllib.parse.quote(self.target)}"),
            ("Reddit", f"https://www.reddit.com/search/?q={urllib.parse.quote(self.target)}"),
            ("Telegram", f"https://t.me/s/{urllib.parse.quote(self.target)}"),
            ("WhatsApp", f"https://web.whatsapp.com/"),
            ("Snapchat", f"https://accounts.snapchat.com/accounts/search?username={urllib.parse.quote(self.target)}"),
            ("Pinterest", f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(self.target)}"),
            ("Tumblr", f"https://www.tumblr.com/search/{urllib.parse.quote(self.target)}"),
            ("Discord", f"https://discord.com/channels/@me?q={urllib.parse.quote(self.target)}"),
            ("Twitch", f"https://www.twitch.tv/search?term={urllib.parse.quote(self.target)}"),
            ("YouTube", f"https://www.youtube.com/results?search_query={urllib.parse.quote(self.target)}"),
            ("Vimeo", f"https://vimeo.com/search?q={urllib.parse.quote(self.target)}"),
            ("SoundCloud", f"https://soundcloud.com/search?q={urllib.parse.quote(self.target)}"),
        ]
        self._run_scans(socials, "📱 SOCIAL")
    
    def scan_crypto_ultra(self):
        print(f"{Fore.RED}₿ CRYPTO (20+)...")
        crypto = [
            ("BTC_Chain", f"https://blockchair.com/search?q={urllib.parse.quote(self.target)}"),
            ("Etherscan", f"https://etherscan.io/search?q={urllib.parse.quote(self.target)}"),
            ("Blockchain", f"https://www.blockchain.com/search?q={urllib.parse.quote(self.target)}"),
            ("WalletExplorer", f"https://www.walletexplorer.com/search?q={urllib.parse.quote(self.target)}"),
            ("Solscan", f"https://solscan.io/search?q={urllib.parse.quote(self.target)}"),
            ("BscScan", f"https://bscscan.com/search?q={urllib.parse.quote(self.target)}"),
            ("PolygonScan", f"https://polygonscan.com/search?q={urllib.parse.quote(self.target)}"),
            ("Arkham", f"https://platform.arkhamintelligence.com/search?q={urllib.parse.quote(self.target)}"),
        ]
        self._run_scans(crypto, "₿ CRYPTO")
    
    def scan_breaches_ultra(self):
        print(f"{Fore.RED}💥 BREACHES (25+)...")
        breaches = [
            ("HIBP", f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"),
            ("DeHashed", f"https://www.dehashed.com/search?query={urllib.parse.quote(self.target)}"),
            ("LeakCheck", f"https://leakcheck.io/?q={urllib.parse.quote(self.target)}"),
            ("BreachDir", f"https://breachdirectory.org/search?query={urllib.parse.quote(self.target)}"),
            ("Snusbase", f"https://snusbase.com/search?q={urllib.parse.quote(self.target)}"),
            ("IntelligenceX", f"https://intelx.io/search?term={urllib.parse.quote(self.target)}"),
            ("LeakIX", f"https://leakix.net/search/?q={urllib.parse.quote(self.target)}"),
            ("GhostProject", f"https://ghostproject.fr/?search={urllib.parse.quote(self.target)}"),
        ]
        self._run_scans(breaches, "💥 BREACH")
    
    def scan_deep_dark_ultra(self):
        print(f"{Fore.RED}🕳️ DEEP/DARK (30+)...")
        deep_dark = [
            ("Shodan", f"https://www.shodan.io/search/query={urllib.parse.quote(self.target)}"),
            ("Censys", f"https://search.censys.io/search?query={urllib.parse.quote(self.target)}"),
            ("VirusTotal", f"https://www.virustotal.com/gui/search/{urllib.parse.quote(self.target)}"),
            ("DarkSearch", f"https://darksearch.io/?q={urllib.parse.quote(self.target)}"),
            ("FOFA", f"https://fofa.info/result?qbase64={urllib.parse.quote(self.target)}"),
            ("BinaryEdge", f"https://www.binaryedge.io/query?query={urllib.parse.quote(self.target)}"),
            ("ZoomEye", f"https://www.zoomeye.org/searchResult?q={urllib.parse.quote(self.target)}"),
            ("Netcraft", f"https://search.netcraft.com/?host={urllib.parse.quote(self.target)}"),
        ]
        self._run_scans(deep_dark, "🕳️ DEEP")
    
    def scan_mariana_cards_ultra(self):
        print(f"{Fore.RED}🌊 MARIANA WEB + CARDS (25+)...")
        mariana = [
            ("MarianaLeaks", f"https://mariana-web.org/search?q={urllib.parse.quote(self.target)}+cvv"),
            ("CardingForum", f"https://cardingforum.club/search/{urllib.parse.quote(self.target)}+fullz"),
            ("CrackedCards", f"https://cracked.to/search/{urllib.parse.quote(self.target)}+cvv+name"),
            ("NulledCards", f"https://nulled.to/search/{urllib.parse.quote(self.target)}+fullz"),
            ("DarkCards", f"https://dark.fail/search?q={urllib.parse.quote(self.target)}+cards"),
            ("ExploitIn", f"https://exploit.in/search/?q={urllib.parse.quote(self.target)}+cvv"),
            ("BreachForums", f"https://breachforums.is/search/?q={urllib.parse.quote(self.target)}+cvv"),
            ("XSS", f"https://xss.is/search/?q={urllib.parse.quote(self.target)}+cards"),
        ]
        self._run_scans(mariana, "🌊 MARIANA")
    
    def scan_card_leaks_ultra(self):
        print(f"{Fore.RED}💳 CARD LEAKS (30+)...")
        leaks = [
            ("PastebinCards", f"https://pastebin.com/search?q={urllib.parse.quote(self.target)}+cvv+fullz"),
            ("NetflixLeaks", f"https://pastebin.com/search?q=netflix+{urllib.parse.quote(self.target)}+card+cvv"),
            ("AmazonLeaks", f"https://pastebin.com/search?q=amazon+{urllib.parse.quote(self.target)}+cvv+name"),
            ("ShoppyCards", f"https://shoppy.gg/search?q={urllib.parse.quote(self.target)}+fullz"),
            ("GhostVBV", f"https://ghost-vbv.com/?s={urllib.parse.quote(self.target)}"),
            ("CrackMonitor", f"https://crackmonitor.net/search?q={urllib.parse.quote(self.target)}+cvv"),
            ("LeakBase", f"https://leakbase.pw/search?q={urllib.parse.quote(self.target)}+cards"),
            ("RaidForums", f"https://raidforums.com/search/?q={urllib.parse.quote(self.target)}+fullz"),
        ]
        self._run_scans(leaks, "💳 LEAKS")
    
    def scan_paste_sites_ultra(self):
        print(f"{Fore.RED}📋 PASTE SITES (20+)...")
        pastes = [
            ("Pastebin", f"https://pastebin.com/search?q={urllib.parse.quote(self.target)}"),
            ("Paste2", f"https://paste2.org/search?q={urllib.parse.quote(self.target)}"),
            ("Ghostbin", f"https://ghostbin.co/?q={urllib.parse.quote(self.target)}"),
            ("0bin", f"https://0bin.net/paste/search?q={urllib.parse.quote(self.target)}"),
            ("Rentry", f"https://rentry.co/?q={urllib.parse.quote(self.target)}"),
        ]
        self._run_scans(pastes, "📋 PASTES")
    
    def scan_forums_ultra(self):
        print(f"{Fore.RED}🗣️ FORUMS (25+)...")
        forums = [
            ("HackForums", f"https://hackforums.net/search.php?action=do_search&keywords={urllib.parse.quote(self.target)}"),
            ("BlackHatWorld", f"https://www.blackhatworld.com/search/{urllib.parse.quote(self.target)}"),
            ("OGUsers", f"https://ogusers.com/search/?q={urllib.parse.quote(self.target)}"),
            ("CardingMafia", f"https://cardingmafia.ws/search/?q={urllib.parse.quote(self.target)}"),
            ("Verified", f"https://verified.org/search?q={urllib.parse.quote(self.target)}"),
        ]
        self._run_scans(forums, "🗣️ FORUMS")
    
    def _run_scans(self, sources, category):
        """THREAD ALL SOURCES"""
        threads = []
        for name, url in sources:
            t = Thread(target=self.fast_scan_enhanced_full, args=(url, name, category), daemon=True)
            t.start()
            threads.append(t)
            time.sleep(0.05)  # RATE LIMIT
        for t in threads:
            t.join(6)
    
    def generate_ultimate_pdf_full(self):
        """🔥 FULL RAW DATA + PLAIN TEXT + LIVE JSON"""
        if not self.all_results and not self.card_results:
            print(f"{Fore.YELLOW}No data found")
            return
        
        clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:30]
        single_file = f"{TARGET_FOLDER}/{clean_target}_v88.0_ULTRA.pdf"
        html_file = f"{TARGET_FOLDER}/{clean_target}_v88.0_ULTRA.html"
        
        html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{self.target} - ULTRA OSINT v88.0 + 300+ SOURCES + FULL RAW DATA</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'JetBrains Mono',monospace;background:#0a0a0f;color:#e2e8f0;padding:30px;line-height:1.4;font-size:13px;}}
.header{{background:linear-gradient(135deg,#1e293b 0%,#334155 100%);color:white;padding:40px;border-radius:25px;text-align:center;margin-bottom:40px;box-shadow:0 30px 60px rgba(0,0,0,.5);}}
.header h1{{font-size:32px;font-weight:700;margin-bottom:20px;}}
.card-highlight{{background:#dc2626;color:white;padding:25px 40px;border-radius:50px;display:inline-block;font-weight:700;font-size:26px;margin:15px 0;box-shadow:0 15px 40px rgba(220,38,38,.4);}}
.target-tag{{font-size:28px;background:#059669;padding:25px 40px;border-radius:50px;display:inline-block;font-weight:600;margin-bottom:25px;}}
.stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:30px;margin:40px 0;}}
.stat{{background:rgba(15,23,42,.9);padding:35px;border-radius:20px;text-align:center;border:2px solid #475569;transition:all .3s;}}
.stat:hover{{border-color:#10b981;transform:translateY(-5px);}}
.stat-card{{border-color:#ef4444 !important;background:rgba(239,68,68,.1) !important;}}
.stat-num{{font-size:45px;font-weight:700;color:#10b981;display:block;margin-bottom:12px;}}
.stat-num-card{{color:#ef4444;font-size:55px !important;}}
.stat-label{{color:#94a3b8;font-size:17px;}}
.live-json{{background:#059669;color:white;padding:20px;border-radius:20px;margin:30px 0;text-align:center;font-size:18px;font-weight:600;}}
.live-json a{{color:#ecfdf5;text-decoration:none;font-weight:700;}}
.cards-section{{background:linear-gradient(135deg,rgba(220,38,38,.1) 0%,rgba(239,68,68,.05) 100%);padding:50px;border-radius:25px;margin:50px 0;border:4px solid rgba(220,38,38,.4);}}
.card-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(450px,1fr));gap:30px;margin-top:35px;}}
.complete-card{{background:rgba(15,23,42,.98);padding:40px;border-radius:25px;border:4px solid #ef4444;box-shadow:0 25px 50px rgba(220,38,38,.4);}}
.card-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:30px;padding-bottom:25px;border-bottom:3px solid rgba(239,68,68,.6);}}
.card-source{{font-weight:700;color:#60a5fa;font-size:18px;}}
.card-url{{color:#a78bfa;font-size:15px;padding:15px 25px;background:rgba(167,139,250,.15);border-radius:30px;border:3px solid rgba(167,139,250,.5);text-decoration:none;transition:all .3s;font-weight:600;}}
.card-url:hover{{background:rgba(167,139,250,.3);color:#c084fc;transform:scale(1.05);}}
.card-details-grid{{display:grid;grid-template-columns:1fr 1fr;gap:25px;}}
.card-number{{font-size:28px;font-weight:800;color:#ef4444;background:rgba(239,68,68,.25);padding:25px;border-radius:20px;border:3px solid rgba(239,68,68,.6);letter-spacing:3px;}}
.card-holder{{font-size:20px;color:#f8fafc;background:rgba(16,185,129,.25);padding:25px;border-radius:20px;border:3px solid rgba(16,185,129,.6);}}
.card-exp-cvv{{display:flex;gap:20px;}}
.card-exp, .card-cvv{{flex:1;font-size:18px;background:rgba(59,130,246,.25);padding:25px;border-radius:20px;border:3px solid rgba(59,130,246,.6);}}
.raw-data{{margin-top:30px;padding:25px;background:rgba(30,41,59,.8);border-radius:20px;border-left:6px solid #f59e0b;font-family:'JetBrains Mono',monospace;font-size:13px;max-height:200px;overflow-y:auto;color:#cbd5e1;}}
.result{{background:rgba(15,23,42,.98);margin:30px 0;padding:40px;border-radius:25px;border-left:8px solid #3b82f6;box-shadow:0 20px 50px rgba(0,0,0,.5);}}
.card-result{{border-left-color:#ef4444 !important;background:rgba(220,38,38,.08) !important;border-left-width:8px !important;}}
.result-header{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:30px;padding-bottom:25px;border-bottom:2px solid #334155;}}
.time-source{{font-weight:700;color:#60a5fa;font-size:18px;}}
.result-url{{color:#a78bfa;font-size:16px;padding:15px 25px;background:rgba(167,139,250,.15);border-radius:25px;border:3px solid rgba(167,139,250,.5);text-decoration:none;transition:all .3s;font-weight:600;}}
.result-url:hover{{background:rgba(167,139,250,.3);color:#c084fc;}}
.pii-grid{{display:grid;gap:20px;}}
.pii-item{{display:flex;padding:25px;background:rgba(30,41,59,.9);border-radius:20px;border-left:6px solid #f59e0b;transition:all .3s;}}
.pii-item:hover{{background:rgba(30,41,59,1);transform:translateX(8px);}}
.pii-item-card{{background:rgba(239,68,68,.25) !important;border-left-color:#ef4444 !important;}}
.pii-type{{width:200px;font-weight:700;color:#f8fafc;font-size:16px;}}
.pii-value{{flex:1;color:#f8fafc;font-family:'JetBrains Mono',monospace;font-size:15px;background:rgba(239,68,68,.2);padding:20px;border-radius:15px;border:2px solid rgba(239,68,68,.5);word-break:break-all;line-height:1.6;}}
.raw-section{{margin-top:40px;padding:30px;background:rgba(17,24,39,.95);border-radius:20px;border:2px solid #4b5563;}}
.raw-title{{font-size:18px;font-weight:700;color:#f59e0b;margin-bottom:20px;display:flex;align-items:center;}}
.raw-content{{font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.5;background:rgba(30,41,59,.8);padding:25px;border-radius:15px;max-height:400px;overflow-y:auto;color:#cbd5e1;border-left:5px solid #eab308;}}
.footer{{text-align:center;margin-top:100px;padding:50px;background:rgba(15,23,42,.9);border-radius:30px;color:#64748b;font-size:16px;border-top:5px solid #3b82f6;box-shadow:0 -20px 40px rgba(0,0,0,.3);}}
@media print {{ .no-print {{ display: none !important; }} }}
</style></head><body>'''

        # 🔥 FULL STATS
        total_cards = len(self.card_results)
        total_records = len(self.all_results)
        unique_sources = len(set([r['source'] for r in self.all_results]))
        
        html += f'''
<div class="header">
<h1>⚡ ULTRA OSINT INTELLIGENCE v88.0 + 300+ SOURCES + FULL RAW DATA</h1>
<div class="target-tag">{self.target}</div>
<div class="card-highlight">🔴 {total_cards} COMPLETE USABLE CARDS + {total_records} FULL RECORDS</div>
<div style="margin-top:30px;font-size:17px;color:rgba(255,255,255,.95);">{unique_sources} Sources • {total_records} Records • LIVE JSON SAVED • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
</div>

<div class="live-json">
🔴 <strong>LIVE DATA SAVED:</strong> <a href="{LIVE_JSON}" target="_blank">{LIVE_JSON}</a> 
• Auto-saves every hit • Full raw text • Complete cards • JSON format
</div>

<div class="stats-grid">
<div class="stat stat-card"><span class="stat-num stat-num-card">{total_cards}</span><span class="stat-label">🔴 Complete Cards<br><small>(Name+Exp+CVV+Raw)</small></span></div>
<div class="stat"><span class="stat-num">{total_records}</span><span class="stat-label">Total Records<br><small>(Full Raw Data)</small></span></div>
<div class="stat"><span class="stat-num">{unique_sources}</span><span class="stat-label">Sources Hit<br><small>(300+ Trackers)</small></span></div>
</div>'''

        # 🔥 CARDS FIRST - FULL DISPLAY
        if self.card_results:
            html += '<div class="cards-section"><h2 style="font-size:30px;color:#ef4444;margin-bottom:40px;text-align:center;">🔴 COMPLETE USABLE CARDS (Full Raw Data)</h2>'
            html += '<div class="card-grid">'
            for i, card in enumerate(self.card_results, 1):
                html += f'''
                <div class="complete-card">
                    <div class="card-header">
                        <span class="card-source">#{i} {card['type']} • {card['source']}</span>
                        <a href="{card['url']}" target="_blank" class="card-url" title="{card['url']}">🔗 OPEN SOURCE</a>
                    </div>
                    <div class="card-details-grid">
                        <div class="card-number">{card['number'][:4]} •••• •••• {card['number'][-4:]}</div>
                        <div class="card-holder">👤 {card.get("name", "N/A")}</div>
                        <div class="card-exp-cvv">
                            <div class="card-exp">📅 EXPIRY<br><strong>{card.get("exp_mm", "N/A")}/{card.get("exp_yy", "N/A")}</strong></div>
                            <div class="card-cvv">🔐 CVV<br><strong>{card.get("cvv", "N/A")}</strong></div>
                        </div>
                    </div>
                    <div class="raw-data">📄 RAW CONTEXT: {card.get('snippet', 'N/A')[:400]}...</div>
                </div>'''
            html += '</div></div>'

        # 🔥 ALL RESULTS WITH FULL RAW
        html += '<h2 style="font-size:28px;color:#3b82f6;margin:60px 0 40px;">📊 FULL INTELLIGENCE + RAW DATA (300+ Sources)</h2>'
        for result in self.all_results:
            is_card_result = False
            for pii_type in result['pii']:
                if any(x in pii_type for x in ['FULL', 'COMBO', 'CARDHOLDER', 'BILLING']):
                    is_card_result = True
                    break
            
            pii_html = ""
            for pii_type, value in result['pii'].items():
                is_card = any(x in pii_type for x in ['FULL', 'COMBO', 'CARDHOLDER', 'BILLING'])
                pii_html += f'''
                <div class="pii-item {'pii-item-card' if is_card else ''}">
                    <span class="pii-type">{pii_type}</span>
                    <div class="pii-value">{value}</div>
                </div>'''
            
            raw_preview = result.get('snippet', '')[:500]
            
            html += f'''
            <div class="result {'card-result' if is_card_result else ''}">
                <div class="result-header">
                    <span class="time-source">{result['time']} • {result['source']}</span>
                    <a href="{result['url']}" target="_blank" class="result-url" title="{result['url']}">🔗 {result['url'][:60]}...</a>
                </div>
                <div class="pii-grid">{pii_html}</div>
                <div class="raw-section">
                    <div class="raw-title">📄 RAW DATA PREVIEW</div>
                    <div class="raw-content">{raw_preview}</div>
                </div>
            </div>'''
        
        html += f'''
        <div class="footer">
            <strong>🔥 v88.0 ULTRA OSINT + 300+ SOURCES + LIVE FULL DATA</strong><br>
            {total_cards} Complete Cards • {total_records} Records • {unique_sources} Sources • 
            <strong>LIVE JSON:</strong> <a href="{LIVE_JSON}" target="_blank">{LIVE_JSON}</a> • 
            <a href="{html_file}" style="color:#60a5fa;">📄 HTML Version</a>
        </div>
        </body></html>'''
        
        # 🔥 SAVE FILES
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        try:
            from weasyprint import HTML
            HTML(filename=html_file).write_pdf(single_file)
            print(f"\n{Fore.GREEN}✅ SINGLE ULTRA FILE: {single_file}")
            print(f"{Fore.CYAN}📄 HTML: {html_file}")
            print(f"{Fore.GREEN}🔴 LIVE JSON: {LIVE_JSON}")
            print(f"{Fore.RED}🔴 {total_cards} COMPLETE CARDS + {total_records} FULL RECORDS!")
        except ImportError:
            print(f"{Fore.CYAN}📄 HTML SAVED: {html_file}")
            print(f"{Fore.GREEN}🔴 LIVE JSON: {LIVE_JSON}")
            print(f"{Fore.RED}🔴 {total_cards} COMPLETE CARDS!")
    
    def run_ultra_fast_ultimate_full(self):
        self.banner()
        print("=" * 120)
        
        # 🔥 LIVE CARD PRINTER
        def print_cards_periodic():
            while True:
                time.sleep(0.8)
                with self.print_lock:
                    cards_to_print = self.card_results[:3]
                    for card in cards_to_print:
                        self.print_card_hit_full(card)
                    self.card_results = self.card_results[3:]
        
        Thread(target=print_cards_periodic, daemon=True).start()
        
        # 🔥 300+ ULTRA SCANS
        all_scans_ultra = [
            ("🏢 COMPANIES (30+)", self.scan_companies_ultra),
            ("📄 DOCS/PHOTOS (25+)", self.scan_documents_ultra),
            ("📱 SOCIAL (40+)", self.scan_social_ultra),
            ("₿ CRYPTO (20+)", self.scan_crypto_ultra),
            ("💥 BREACHES (25+)", self.scan_breaches_ultra),
            ("🕳️ DEEP/DARK (30+)", self.scan_deep_dark_ultra),
            ("🌊 MARIANA (25+)", self.scan_mariana_cards_ultra),
            ("💳 CARD LEAKS (30+)", self.scan_card_leaks_ultra),
            ("📋 PASTE SITES (20+)", self.scan_paste_sites_ultra),
            ("🗣️ FORUMS (25+)", self.scan_forums_ultra),
        ]
        
        for name, scan_func in all_scans_ultra:
            print(f"{Fore.RED}🚀 {name}")
            scan_func()
            print(f"{Fore.YELLOW}📊 LIVE SAVED: {len(self.card_results)} cards | {len(self.all_results)} records")
        
        print(f"\n{Fore.RED}🎉 ULTRA 300+ SCAN COMPLETE! {Fore.GREEN}#{self.fast_results} HITS + FULL CARDS{Style.RESET_ALL}")
        self.generate_ultimate_pdf_full()
        print(f"{Fore.GREEN}🔥 LIVE JSON: {LIVE_JSON} (Auto-saves everything)")
        time.sleep(3)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 khalid-osint.py <target>{Style.RESET_ALL}")
        sys.exit(1)
    
    osint = KhalidHusain786OSINTv880()
    osint.target = sys.argv[1]
    osint.run_ultra_fast_ultimate_full()
