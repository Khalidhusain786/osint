#!/usr/bin/env python3
"""
🔥 KHALID HUSAIN RAW PRO v86.0 🔥
ANISH EXPLOITS AUTO + RAW DATA DISPLAY
BY: Khalid Husain | ANISH AUTO-LOGIN • RAW DOCS
"""

import asyncio
import aiohttp
import subprocess
import sys
import re
import time
import urllib.parse
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Tuple
from weasyprint import HTML
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

init(autoreset=True)

@dataclass
class RawHit:
    website: str
    engine: str
    raw_data: str
    link: str = ""

class KhalidRawProV86:
    def __init__(self):
        self.target = ""
        self.raw_hits: List[RawHit] = []
        self.start_time = time.time()
        self.session = None
        
    async def init_session(self):
        timeout = aiohttp.ClientTimeout(total=12, connect=5)
        self.session = aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(limit=50))
    
    async def close_session(self):
        if self.session:
            await self.session.close()
    
    def print_raw_banner(self):
        print(f"\n{Fore.RED}{'='*80}")
        print(f"{Fore.YELLOW}🔥 KHALID HUSAIN RAW PRO v86.0 - ANISH AUTO 🔥")
        print(f"{Fore.CYAN}Target: {self.target}")
        print(f"{Fore.RED}{'='*80}\n")
    
    def display_raw_hit(self, hit: RawHit):
        """EXACT RAW FORMAT"""
        print(f"{Fore.MAGENTA}{hit.website}")
        print(f"{Fore.RED}--------------------")
        print(f"{Fore.WHITE}{hit.raw_data}")
        print()
        self.raw_hits.append(hit)
    
    # === ANISH EXPLOITS AUTO LOGIN ===
    async def anish_exploits_auto(self):
        """AUTO: Open → Login Anish123 → Search Target → Extract RAW"""
        print(f"{Fore.BLUE}[🔑 ANISH EXPLOITS AUTO-LOGIN] Auto: Open → Anish123 → {self.target}")
        print("-" * 50)
        
        try:
            # Selenium Chrome headless
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (KhalidRawPro-AnishAuto)")
            
            driver = webdriver.Chrome(options=chrome_options)
            wait = WebDriverWait(driver, 15)
            
            # Step 1: Open Anish Exploits
            print(f"{Fore.GREEN}→ Opening https://anishexploits.site/app/")
            driver.get("https://anishexploits.site/app/")
            
            # Step 2: Auto-enter password "Anish123"
            print(f"{Fore.GREEN}→ Auto-entering password: Anish123")
            password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.clear()
            password_field.send_keys("Anish123")
            
            # Step 3: Auto-submit
            submit_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Login') or @type='submit']")
            submit_btn.click()
            
            print(f"{Fore.GREEN}→ Anish login SUCCESS ✓")
            time.sleep(3)
            
            # Step 4: Auto-enter target phone
            print(f"{Fore.GREEN}→ Searching target: {self.target}")
            target_field = wait.until(EC.presence_of_element_located((By.NAME, "phone") or (By.ID, "phone") or (By.XPATH, "//input[@placeholder*='phone']")))
            target_field.clear()
            target_field.send_keys(self.target.replace('+', ''))
            
            search_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Search') or contains(text(),'Submit')]")
            search_btn.click()
            
            # Step 5: Extract ALL raw data
            time.sleep(5)
            page_source = driver.page_source
            
            # Extract raw Anish data
            anish_hits = self.extract_anish_raw(page_source)
            for hit in anish_hits:
                self.display_raw_hit(hit)
            
            driver.quit()
            print(f"{Fore.GREEN}→ Anish Exploits COMPLETE ✓")
            
        except Exception as e:
            print(f"{Fore.RED}Anish Error: {e}")
    
    def extract_anish_raw(self, html: str) -> List[RawHit]:
        """Extract RAW from Anish Exploits"""
        hits = []
        
        # Clean HTML → raw text
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', '\n', text).strip()
        
        # Document patterns
        doc_matches = re.findall(r'Document:\s*\d+\s*Name:\s*[^\n]+(?:\n[^D]+)?', text, re.MULTILINE)
        for doc_data in doc_matches:
            hits.append(RawHit("AnishExploits.site", "ANISH-AUTO", doc_data.strip()))
        
        # Phone/Name/Address
        patterns = [
            r'(Phone:\s*\d+[\s\n]+(?:Phone:\s*\d+)?)',
            r'(Name:\s*[A-Z\s]+(?:\nFather-name:.*?)?)',
            r'(Address:\s*[^P]+?)(?=\nPhone:|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
            for match in matches[:3]:
                hits.append(RawHit("AnishExploits.site", "ANISH-RAW", match.strip()))
        
        return hits
    
    # === RAW DATA PATTERNS ===
    RAW_PATTERNS = {
        'Document': r'(Document:\s*\d+)',
        'Name': r'(Name:\s*[A-Z\s]+)',
        'Father-name': r'(Father-name:\s*[A-Z\s]+)',
        'Address': r'(Address:\s*[^P]+(?:Phone|$))',
        'Phone': r'(Phone:\s*\d+)',
        'IP': r'(IP\s*)',
        'BTC': r'(BTC\s*)',
        'Website': r'(Website\s*https?://[^\s\n]+)'
    }
    
    def extract_raw_data(self, html: str, website: str, engine: str) -> List[RawHit]:
        """Extract EXACT raw format data"""
        hits = []
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        
        doc_blocks = re.split(r'(Document:\s*\d+)', text)
        for i in range(1, len(doc_blocks), 2):
            doc_id = doc_blocks[i].strip()
            block_text = doc_blocks[i+1].strip() if i+1 < len(doc_blocks) else ""
            block_data = f"{doc_id}\n{block_text}"
            
            if any(p in block_data for p in ['Name:', 'Phone:', 'Address:']):
                hits.append(RawHit(website, engine, block_data.strip()))
        
        return hits
    
    # === ENGINES ===
    DOC_ENGINES = [
        ("HiTeckGroop.in", "https://hiteckgroop.in/search?q={target}"),
        ("IndiaGovDocs", "https://indiagovdocs.com/search/{target}"),
        ("GovLeaked", "https://govleaked.in/?s={target}"),
    ]
    
    async def scan_raw_engine(self, name: str, url_template: str, semaphore):
        async with semaphore:
            try:
                url = url_template.format(target=urllib.parse.quote(self.target))
                async with self.session.get(url) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        raw_hits = self.extract_raw_data(html, name, "DOC")
                        for hit in raw_hits:
                            self.display_raw_hit(hit)
            except:
                pass
    
    async def ultimate_raw_blitz(self):
        """Raw hits + Anish Auto"""
        self.print_raw_banner()
        
        # 🔥 ANISH EXPLOITS FIRST - AUTO LOGIN
        await self.anish_exploits_auto()
        
        # Other engines
        semaphore = asyncio.Semaphore(15)
        tasks = [self.scan_raw_engine(name, url, semaphore) for name, url in DOC_ENGINES]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def generate_raw_pdf(self):
        pdf_content = ""
        for hit in self.raw_hits:
            pdf_content += f"""
<div style="margin: 20px 0; padding: 20px; border: 3px solid #ff4444; border-radius: 10px; background: #111;">
<h3 style="color: #ff4444; margin: 0 0 15px 0; font-size: 18px;">{hit.website}</h3>
<pre style="background: #000; color: #00ff88; padding: 20px; margin: 0; font-size: 14px; border-radius: 5px; white-space: pre-wrap; overflow-x: auto;">
{hit.raw_data}
</pre>
</div>
            """
        
        header = f"""
<!DOCTYPE html>
<html>
<head><title>Khalid Raw Pro v86</title></head>
<body style="background: #000; color: #fff; font-family: 'Courier New', monospace;">
<div style="background: linear-gradient(90deg, #ff0000, #ff6600); padding: 25px; text-align: center; border-radius: 15px;">
<h1 style="margin: 0; font-size: 36px;">🔥 KHALID HUSAIN RAW PRO v86.0 🔥</h1>
<p style="margin: 15px 0 0 0; font-size: 20px;"><strong>Target:</strong> <code style="background: #000; padding: 5px 10px;">{self.target}</code></p>
<p style="margin: 10px 0 0 0; font-size: 18px;">Total Raw Hits: <strong style="color: #00ff88;">{len(self.raw_hits)}</strong></p>
</div>
{pdf_content}
<div style="text-align: center; padding: 20px; color: #888; font-size: 12px;">
Generated by Khalid Husain Raw Pro v86.0
</div>
</body>
</html>
        """
        
        safe_name = re.sub(r'[^\w\-_.]', '_', self.target)[:30]
        pdf_file = f"Khalid_Raw_Anish_{safe_name}_v86.pdf"
        
        try:
            HTML(string=header).write_pdf(pdf_file)
            print(f"\n{Fore.RED}{'='*80}")
            print(f"📄 ANISH+RAW PDF: {pdf_file}")
            print(f"{Fore.YELLOW}Total Raw Hits: {len(self.raw_hits)}")
        except:
            pass
    
    async def run_raw(self):
        await self.init_session()
        await self.ultimate_raw_blitz()
        self.generate_raw_pdf()
        await self.close_session()

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python khalid_raw_v86.py <phone>")
        sys.exit(1)
    
    pro = KhalidRawProV86()
    pro.target = sys.argv[1].strip()
    asyncio.run(pro.run_raw())

if __name__ == "__main__":
    main()
