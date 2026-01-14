#!/usr/bin/env python3
"""
🔥 KHALID HUSAIN PENTEST PRO v85.0 🔥
CLEAN HITS ONLY - RAW DATA DISPLAY
BY: Khalid Husain | RAW DOCS • PHONE • EXACT FORMAT
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
import os

init(autoreset=True)

@dataclass
class RawHit:
    website: str
    engine: str
    raw_data: str
    link: str = ""

class KhalidRawProV85:
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
        print(f"{Fore.YELLOW}🔥 KHALID HUSAIN RAW HITS v85.0 🔥")
        print(f"{Fore.CYAN}Target: {self.target}")
        print(f"{Fore.RED}{'='*80}\n")
    
    def display_raw_hit(self, hit: RawHit):
        """EXACT RAW FORMAT - No extra text"""
        print(f"{Fore.MAGENTA}{hit.website}")
        print(f"{Fore.RED}--------------------")
        print(f"{Fore.WHITE}{hit.raw_data}")
        print()
        self.raw_hits.append(hit)
    
    # === RAW DATA PATTERNS ===
    RAW_PATTERNS = {
        'Document': r'(Document:\s*\d+)',
        'Name': r'(Name:\s*[A-Z\s]+)',
        'Father-name': r'(Father-name:\s*[A-Z\s]+)',
        'Address': r'(Address:\s*[^P]+(?:Phone|$))',
        'Phone': r'(Phone:\s*\d+)',
        'IP': r'(IP\s*)',
        'BTC': r'(BTC\s*)',
        'Website': r'(Website\s*https?://[^\s]+)'
    }
    
    def extract_raw_data(self, html: str, website: str, engine: str) -> List[RawHit]:
        """Extract EXACT raw format data"""
        hits = []
        
        # Clean HTML for raw text extraction
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Find document blocks
        doc_blocks = re.split(r'(Document:\s*\d+)', text)
        
        for i in range(1, len(doc_blocks), 2):
            doc_id = doc_blocks[i].strip()
            block_text = doc_blocks[i+1].strip() if i+1 < len(doc_blocks) else ""
            
            # Extract all patterns from block
            block_data = f"{doc_id}\n{block_text}"
            
            if any(pattern in block_data for pattern in ['Name:', 'Phone:', 'Address:']):
                hits.append(RawHit(website, engine, block_data.strip()))
        
        # Single hits (IP, BTC, Website)
        for type_, pattern in RAW_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches[:2]:
                hits.append(RawHit(website, engine, match.strip()))
        
        return hits
    
    # === TARGETED ENGINES ===
    DOC_ENGINES = [
        ("HiTeckGroop.in", "https://hiteckgroop.in/search?q={target}"),
        ("IndiaGovDocs", "https://indiagovdocs.com/search/{target}"),
        ("GovLeaked", "https://govleaked.in/?s={target}"),
        ("DocumentLeak", "https://documentleak.site/search?q={target}"),
    ]
    
    PHONE_ENGINES = [
        ("Truecaller", "https://www.truecaller.com/search/in/{target}"),
        ("PhoneLeak", "https://phoneleak.com/{target}"),
        ("NumLookup", "https://www.numlookup.com/{target}"),
    ]
    
    async def scan_raw_engine(self, name: str, url_template: str, semaphore):
        """Scan for RAW hits only"""
        async with semaphore:
            try:
                url = url_template.format(target=urllib.parse.quote(self.target))
                async with self.session.get(url, headers={'User-Agent': 'KhalidRawPro'}) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        raw_hits = self.extract_raw_data(html, name, "DOC_SEARCH")
                        for hit in raw_hits:
                            self.display_raw_hit(hit)
            except:
                pass
    
    async def kali_raw_scan(self):
        """Kali tools - raw output only"""
        print(f"{Fore.BLUE}[KALI RAW]")
        print("-" * 20)
        
        cmds = [
            f"grep -r '{self.target}' /usr/share/wordlists/ 2>/dev/null | head -10",
            f"theHarvester -d {self.target} -b google -l 20 2>/dev/null | grep -E 'Phone|Name|Address'",
        ]
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=3) as executor:
            tasks = [loop.run_in_executor(executor, self.run_raw_kali, cmd) for cmd in cmds]
            await asyncio.gather(*tasks)
    
    def run_raw_kali(self, cmd: str):
        """Raw Kali output"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            if result.stdout.strip():
                self.display_raw_hit(RawHit("KaliLinux", cmd.split()[0], result.stdout.strip()))
        except:
            pass
    
    async def ultimate_raw_blitz(self):
        """Raw hits only"""
        self.print_raw_banner()
        
        semaphore = asyncio.Semaphore(20)
        
        # Document engines
        doc_tasks = [self.scan_raw_engine(name, url, semaphore) for name, url in DOC_ENGINES]
        phone_tasks = [self.scan_raw_engine(name, url, semaphore) for name, url in PHONE_ENGINES]
        
        await asyncio.gather(*(doc_tasks + phone_tasks), return_exceptions=True)
        await self.kali_raw_scan()
    
    def generate_raw_pdf(self):
        """Raw PDF - clickable links"""
        pdf_content = ""
        
        for hit in self.raw_hits:
            pdf_content += f"""
<div style="margin: 15px 0; padding: 15px; border: 2px solid #ff4444; border-radius: 8px;">
<h3 style="color: #ff4444; margin: 0 0 10px 0;">{hit.website}</h3>
<div style="background: #1a1a1a; color: #00ff00; padding: 15px; font-family: monospace; font-size: 14px; white-space: pre-wrap;">
{hit.raw_data}
</div>
{hit.link and f'<p><a href="{hit.link}" target="_blank" style="color: #00aaff;">🔗 OPEN LINK</a></p>' or ''}
</div>
            """
        
        header = f"""
<!DOCTYPE html>
<html>
<head><title>Khalid Husain Raw Hits</title></head>
<body style="background: #000; color: #fff; font-family: Arial;">
<div style="background: linear-gradient(90deg, #ff0000, #ff6600); padding: 20px; text-align: center;">
<h1 style="margin: 0; font-size: 32px;">🔥 KHALID HUSAIN RAW HITS v85.0 🔥</h1>
<p style="margin: 10px 0 0 0; font-size: 18px;"><strong>Target:</strong> <code>{self.target}</code></p>
<p style="margin: 5px 0 0 0;">Total Raw Hits: <strong>{len(self.raw_hits)}</strong></p>
</div>
{pdf_content}
</body>
</html>
        """
        
        safe_name = re.sub(r'[^\w\-_.]', '_', self.target)[:30]
        pdf_file = f"Khalid_Raw_{safe_name}_v85.pdf"
        
        try:
            HTML(string=header).write_pdf(pdf_file)
            print(f"\n{Fore.GREEN}{'='*80}")
            print(f"📄 RAW PDF SAVED: {pdf_file}")
            print(f"{Fore.YELLOW}Total Raw Hits Found: {len(self.raw_hits)}")
            print(f"{Fore.RED}{'='*80}")
        except:
            pass
    
    async def run_raw(self):
        await self.init_session()
        await self.ultimate_raw_blitz()
        self.generate_raw_pdf()
        await self.close_session()

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python khalid_raw_v85.py <target>")
        sys.exit(1)
    
    pro = KhalidRawProV85()
    pro.target = sys.argv[1].strip()
    asyncio.run(pro.run_raw())

if __name__ == "__main__":
    main()
