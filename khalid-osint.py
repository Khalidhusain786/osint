import asyncio
import aiohttp
from playwright.async_api import async_playwright
import stem.control
from stem import Signal
import random
import re
import json
from datetime import datetime
import folium
import streamlit as st
from pyvis.network import Network
import pandas as pd
import os

# Mariana Web .onion markets (Deep Web Elite)
MARIANA_DEEP_WEB = [
    "http://marianaonionxxx.onion",  # Mariana Web markets
    "http://deepwebmariana.onion",
    "http://shadowmariana.onion",
    "http://darkmarianamarket.onion",
    "http://eliteoniondeep.onion",
    "http://cryptomarianadark.onion",
    "http://deepshadowmarket.onion",
    "http://marianaelite.onion",
    "http://darknetmarianadump.onion",
    "http://shadowdeepmarket.onion"
]

# Combined REAL + MARIANA
ALL_ONION_MARKETS = REAL_ONION_MARKETS + MARIANA_DEEP_WEB

class EliteOnionCollector:
    def __init__(self, target):
        self.target = target
        self.tor_proxies = ['socks5h://127.0.0.1:9050']
        self.current_proxy_idx = 0
        self.vendors = []
        self.drops = []
        self.wallets = []
        self.emails = []
        self.phones = []
        self.domains = []
        self.api_keys = []
        
        # Controller for printing individual items
        self.found_items = {
            'vendors': [], 'drops': [], 'wallets': [],
            'emails': [], 'phones': [], 'domains': []
        }
        
    async def init_tor_rotation(self):
        """🔄 Tor circuit rotation"""
        try:
            self.controller = stem.control.Controller.from_port(port=9051)
            self.controller.authenticate()
        except:
            print("⚠️ Stem controller not available - using static proxy")
    
    def rotate_tor(self):
        """🔄 Rotate Tor circuit"""
        try:
            self.controller.signal(Signal.NEWNYM)
            print(f"🔄 Tor circuit rotated")
        except:
            pass
    
    def get_session(self):
        """🌐 Tor proxy session"""
        proxy = self.tor_proxies[0]
        connector = aiohttp.TCPConnector(limit=5)
        session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=45),
            headers={'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            ])}
        )
        return session
    
    async def stealth_scrape(self, url):
        """🕵️ Playwright + Tor stealth scraping"""
        print(f"🔍 Scraping: {url}")
        self.rotate_tor()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, proxy={'server': 'socks5://127.0.0.1:9050'})
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until='networkidle', timeout=60000)
                await asyncio.sleep(random.uniform(3, 7))  # Human delay
                
                # Simulate scrolling
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
                await asyncio.sleep(random.uniform(1, 3))
                
                html = await page.content()
                await browser.close()
                return html
            except Exception as e:
                print(f"❌ Scrape failed: {e}")
                await browser.close()
                return None
    
    def extract_all_iocs(self, html):
        """🔍 NO API - Pure regex extraction"""
        iocs = {}
        
        # Enhanced regex (NO APIs)
        patterns = {
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phones': r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            'domains': r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b(?!\.onion)',
            'btc': r'(?:bc1[0-9a-zA-Z]{39,59}|1[0-9A-Za-km-z]{25,34}|3[0-9A-Za-km-z]{25,34})',
            'eth': r'0x[a-fA-F0-9]{40}',
            'vendors': r'(?:vendor|seller|shop)[\s:]*([A-Za-z0-9\s\-_]{3,30})',
            'drops': r'(?:drop|ship|address|location)[\s:]*([A-Za-z0-9\s\.,\-#]{10,})'
        }
        
        for ioc_type, pattern in patterns.items():
            iocs[ioc_type] = re.findall(pattern, html, re.IGNORECASE)
        
        return iocs
    
    def print_individual_items(self, iocs, source):
        """📱 Screen pe individual items print"""
        print(f"\n{'='*60}")
        print(f"🎯 TARGET: {self.target}")
        print(f"🌐 SOURCE: {source}")
        print(f"{'='*60}")
        
        # Vendors
        if iocs.get('vendors'):
            print(f"\n👤 VENDORS FOUND ({len(iocs['vendors'])}):")
            for i, vendor in enumerate(set(iocs['vendors'])[:10], 1):
                clean_vendor = re.sub(r'[^\w\s\-]', '', vendor.strip())
                if len(clean_vendor) > 3:
                    print(f"   {i}. {clean_vendor}")
                    self.found_items['vendors'].append(clean_vendor)
        
        # Wallets
        btc_wallets = iocs.get('btc', [])
        eth_wallets = iocs.get('eth', [])
        if btc_wallets or eth_wallets:
            print(f"\n💰 WALLETS FOUND ({len(btc_wallets)+len(eth_wallets)}):")
            for i, wallet in enumerate(btc_wallets + eth_wallets, 1):
                print(f"   {i}. {wallet}")
                self.found_items['wallets'].append(wallet)
                self.wallets.append(wallet)
        
        # Emails
        if iocs.get('emails'):
            print(f"\n📧 EMAILS FOUND ({len(iocs['emails'])}):")
            for i, email in enumerate(set(iocs['emails'])[:20], 1):
                print(f"   {i}. {email}")
                self.found_items['emails'].append(email)
                self.emails.append(email)
        
        # Phones
        if iocs.get('phones'):
            print(f"\n📱 PHONES FOUND ({len(iocs['phones'])}):")
            for i, phone in enumerate(set(iocs['phones'])[:10], 1):
                clean_phone = ''.join(phone)
                print(f"   {i}. {clean_phone}")
                self.found_items['phones'].append(clean_phone)
                self.phones.append(clean_phone)
        
        # Domains
        if iocs.get('domains'):
            print(f"\n🌐 DOMAINS FOUND ({len(iocs['domains'])}):")
            for i, domain in enumerate(set(iocs['domains'])[:15], 1):
                print(f"   {i}. {domain}")
                self.found_items['domains'].append(domain)
                self.domains.append(domain)
        
        # Drops
        if iocs.get('drops'):
            print(f"\n📦 DROPS FOUND ({len(iocs['drops'])}):")
            for i, drop in enumerate(set(iocs['drops'])[:10], 1):
                clean_drop = ' '.join(drop.split())[:100]
                print(f"   {i}. {clean_drop}")
                self.found_items['drops'].append(clean_drop)
                self.drops.append({'name': f"Drop-{i}", 'address': clean_drop})
        
        print(f"{'='*60}\n")
    
    async def scrape_mariana_markets(self):
        """🌑 Mariana Web + Deep Web scraping"""
        print(f"\n🕳️  MARIANA WEB SCAN STARTED...")
        print(f"   Markets: {len(MARIANA_DEEP_WEB)}")
        
        for i, market in enumerate(MARIANA_DEEP_WEB, 1):
            print(f"\n[{i}/{len(MARIANA_DEEP_WEB)}] 🌑 {market}")
            html = await self.stealth_scrape(market)
            
            if html:
                iocs = self.extract_all_iocs(html)
                self.print_individual_items(iocs, market)
                
                # Add to main lists
                self.vendors.extend(self.found_items['vendors'][:5])
                
                await asyncio.sleep(random.uniform(8, 15))  # Stealth delay
        
        print("✅ MARIANA WEB SCAN COMPLETE")
    
    async def collect_all(self):
        """🚀 Full collection - Mariana + Real markets"""
        await self.init_tor_rotation()
        
        # Mariana first
        await self.scrape_mariana_markets()
        
        # Then real markets
        print(f"\n💎 REAL MARKET SCAN...")
        for market in REAL_ONION_MARKETS[:5]:  # Limited for demo
            print(f"🔍 {market}")
            html = await self.stealth_scrape(market)
            if html:
                iocs = self.extract_all_iocs(html)
                self.print_individual_items(iocs, market)
            await asyncio.sleep(random.uniform(5, 10))
        
        self.print_final_summary()
    
    def print_final_summary(self):
        """📊 Final screen summary"""
        print(f"\n{'🔥 FINAL ELITE SUMMARY 🔥'}")
        print(f"{'='*50}")
        print(f"🎯 TARGET: {self.target}")
        print(f"👥 VENDORS: {len(set(self.found_items['vendors']))}")
        print(f"💰 WALLETS: {len(self.wallets)}")
        print(f"📧 EMAILS: {len(self.emails)}")
        print(f"📱 PHONES: {len(self.phones)}")
        print(f"🌐 DOMAINS: {len(self.domains)}")
        print(f"📦 DROPS: {len(self.drops)}")
        print(f"{'='*50}")

async def main():
    print("""
💎 ELITE MARIANA COLLECTOR v6.0 - NO APIs
┌─────────────────────────────────────────────────────┐
│  Mariana Web • Deep Markets • Stealth Scraping      │
│  Individual Item Display • Pure Regex Extraction    │
│              DARK WEB INTEL SUITE                    │
└─────────────────────────────────────────────────────┘
    """)
    
    target = input("🎯 Elite Target: ").strip()
    
    os.makedirs("iocs", exist_ok=True)
    collector = EliteOnionCollector(target)
    
    await collector.collect_all()
    
    # Save results
    results = {
        'target': target,
        'vendors': list(set(collector.found_items['vendors'])),
        'wallets': collector.wallets,
        'emails': collector.emails,
        'phones': collector.phones,
        'domains': collector.domains,
        'drops': collector.drops
    }
    
    with open(f"iocs/{target}_mariana_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved: iocs/{target}_mariana_results.json")
    print("🎉 MARIANA WEB ELITE COLLECTION COMPLETE!")

if __name__ == "__main__":
    asyncio.run(main())
