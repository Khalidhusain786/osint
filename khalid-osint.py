
```python
#!/usr/bin/env python3
"""
Ultimate OSINT v85.0 - FIXED + ENHANCED + TARGET-NAMED PDF ONLY
WORLDWIDE COVERAGE + TELEGRAM + AUTO EXPLOITS + CLICKABLE LINKS
"""

import os, subprocess, sys, requests, re, time, random, json, shlex, webbrowser
from colorama import Fore, Style, init
from threading import Thread, Lock
from bs4 import BeautifulSoup
import markdown
from weasyprint import HTML
import urllib.parse
from datetime import datetime
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

init(autoreset=True)
print_lock = Lock()

class UltimateOSINTv85:
    def __init__(self):
        self.target = ""
        self.results = []
        self.pdf_content = ""
        self.tor_running = False
        self.telegram_bot_token = ""
        self.telegram_chat_id = ""
        self.search_engines = []
        
    def print_clean_hit(self, category, data, source, engine, link=""):
        """CLEAN console output - ONLY confirmed data"""
        with print_lock:
            print(f"{Fore.RED}✓{Fore.WHITE} {category:12} | {Fore.CYAN}{source} ({engine}){Style.RESET_ALL}")
            print(f"   {Fore.YELLOW}{data}{Style.RESET_ALL}")
            if link:
                print(f"   {Fore.BLUE}🔗 {link} {Style.RESET_ALL}")
            print()
        
        # Store for PDF
        self.results.append({
            "category": category, 
            "data": data, 
            "source": source, 
            "engine": engine, 
            "link": link
        })
        
        self.send_telegram_alert(category, data, source, engine, link)
    
    def categorize_data(self, data, html_context=""):
        """Smart data categorization"""
        patterns = {
            'NAME': r'(?:Name|Full Name|Username)[:\s]*([A-Za-z\s]+?)(?:\s|$|<)',
            'PHONE': r'[\+]?[6-9]\d{9,10}',
            'PINCODE': r'\b[1-9][0-9]{5}\b',
            'PAN': r'[A-Z]{5}[0-9]{4}[A-Z]',
            'VEHICLE': r'[A-Z]{2}[0-9]{1,2}[A-Z]{2}\d{4}',
            'LOCATION': r'(?:Location|City|Country|Address)[:\s]*([A-Za-z\s,]+?)(?:\s|$|<)',
            'USERNAME': r'(?:@|Instagram|Twitter|Facebook)[:\s]*([a-zA-Z0-9_]+)',
            'DOMAIN': r'\b(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9][a-z0-9-]*[a-z0-9]\b',
            'IP': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'BTC': r'1[1-9A-HJ-NP-Za-km-z]{32,33}|3[1-9A-HJ-NP-Za-km-z]{32,33}|bc1[a-z0-9]{39,59}',
            'EMAIL': r'[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}'
        }
        
        for category, pattern in patterns.items():
            matches = re.findall(pattern, data + ' ' + html_context, re.IGNORECASE)
            for match in matches:
                clean_match = re.sub(r'[^\w\s@.\-+]', '', match.strip())[:50]
                if len(clean_match) > 3 and self.target not in clean_match or len(clean_match) > 10:
                    return category, clean_match
        return "DATA", data[:50]
    
    def scan_url_enhanced(self, url, source, engine="WEB"):
        """Enhanced scanner with categorization"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            res = requests.get(url, headers=headers, timeout=15)
            html = res.text
            
            # Extract ALL text content
            soup = BeautifulSoup(html, 'html.parser')
            text_content = soup.get_text()
            
            # Find target context
            if self.target.lower() in text_content.lower():
                context_start = text_content.lower().find(self.target.lower())
                context_snippet = text_content[max(0, context_start-100):context_start+200]
                
                category, clean_data = self.categorize_data(self.target, context_snippet)
                self.print_clean_hit(category, clean_data, source, engine, url)
                
        except:
            pass
    
    def auto_anishexploits_fixed(self):
        """FIXED Auto Anishexploits"""
        print(f"{Fore.RED}[💥 ANISHEXPLoITS.SITE AUTO]")
        try:
            chrome_options = uc.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = uc.Chrome(options=chrome_options)
            driver.get("https://anishexploits.site/")
            time.sleep(5)
            
            # Search for target
            search_box = driver.find_element(By.TAG_NAME, "input")
            search_box.send_keys(self.target)
            search_box.submit()
            
            time.sleep(5)
            html = driver.page_source
            category, data = self.categorize_data(self.target, html)
            self.print_clean_hit(category, data, "Anishexploits", "CHROME", "https://anishexploits.site/")
            
            driver.quit()
        except Exception as e:
            print(f"{Fore.YELLOW}[ANISH] {str(e)[:60]}")
    
    def kali_enhanced(self):
        """Enhanced Kali with categorization"""
        print(f"{Fore.RED}[⚔️ KALI SUITE]")
        tools = ['nmap', 'subfinder']
        
        for tool in tools:
            if subprocess.run(['which', tool], capture_output=True).returncode == 0:
                cmd = f"{tool} {self.target}"
                try:
                    result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=120)
                    if result.stdout:
                        category, data = self.categorize_data(self.target, result.stdout)
                        self.print_clean_hit(category, data, tool.upper(), "KALI", f"kali://{tool}")
                except:
                    pass
    
    def worldwide_fixed(self):
        """FIXED Worldwide coverage"""
        print(f"{Fore.MAGENTA}[🌍 WORLDWIDE]")
        sources = [
            ("HIBP", f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(self.target)}"),
            ("LeakCheck", f"https://leakcheck.io/?q={urllib.parse.quote(self.target)}"),
            ("VirusTotal", f"https://www.virustotal.com/gui/search/{urllib.parse.quote(self.target)}"),
            ("Shodan", f"https://www.shodan.io/search?query={urllib.parse.quote(self.target)}"),
        ]
        
        threads = []
        for source, url in sources:
            t = Thread(target=self.scan_url_enhanced, args=(url, source, "FIREFOX"), daemon=True)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=30)
    
    def generate_target_pdf(self):
        """TARGET-NAMED PDF ONLY - No extra paths"""
        if not self.results:
            print(f"{Fore.YELLOW}No results found")
            return
        
        safe_target = re.sub(r'[^\w\-_.]', '_', self.target)[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        pdf_filename = f"{safe_target}_OSINT_v85_{timestamp}.pdf"
        
        # Beautiful PDF content
        pdf_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OSINT v85 - {self.target}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #dc3545; border-bottom: 3px solid #dc3545; padding-bottom: 10px; }}
        .header {{ background: linear-gradient(90deg, #dc3545, #007bff); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
        .hit {{ background: #f8f9fa; margin: 15px 0; padding: 20px; border-left: 5px solid #007bff; border-radius: 5px; }}
        .category {{ font-weight: bold; color: #dc3545; font-size: 14px; text-transform: uppercase; }}
        .data {{ font-size: 18px; color: #333; margin: 10px 0; }}
        .source {{ color: #666; font-size: 12px; }}
        .link {{ color: #007bff; text-decoration: none; }}
        .link:hover {{ text-decoration: underline; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ background: #e9ecef; padding: 10px 20px; border-radius: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f1f3f4; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 ULTIMATE OSINT v85.0 - WORLDWIDE PENTEST</h1>
        <div class="stats">
            <div class="stat"><strong>{self.target}</strong></div>
            <div class="stat"><strong>{len(self.results)}</strong> Hits</div>
            <div class="stat"><strong>{datetime.now().strftime('%Y-%m-%d %H:%M')}</strong></div>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th><strong>CATEGORY</strong></th>
                <th><strong>DATA</strong></th>
                <th><strong>SOURCE</strong></th>
                <th><strong>ENGINE</strong></th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Add all results
        for result in self.results:
            pdf_html += f"""
            <tr>
                <td><span class="category">{result['category']}</span></td>
                <td><strong class="data">{result['data']}</strong></td>
                <td class="source">{result['source']}</td>
                <td class="source">{result['engine']}</td>
            </tr>
            """
        
        pdf_html += """
        </tbody>
    </table>
</body>
</html>
        """
        
        # Generate PDF in current directory ONLY
        HTML(string=pdf_html).write_pdf(pdf_filename)
        print(f"\n{Fore.GREEN}📄 TARGET PDF SAVED: {pdf_filename}")
        print(f"{Fore.BLUE}🔗 Double-click to open or use: open {pdf_filename}")
    
    def send_telegram_alert(self, category, data, source, engine, link=""):
        """Telegram alerts"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return
        try:
            message = f"🎯 *{category}*\n`{data}`\n*{source} ({engine})*"
            if link: message += f"\n🔗 {link}"
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            requests.post(url, data={
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            })
        except:
            pass
    
    def ultimate_scan_v85(self):
        """Main execution - CLEAN + FAST"""
        print(f"{Fore.RED}⚔️ ULTIMATE OSINT v85.0 - FIXED")
        print(f"{Fore.CYAN}🎯 Target: {self.target}")
        print("=" * 70)
        
        # Run all scanners
        threads = [
            Thread(target=self.kali_enhanced, daemon=True),
            Thread(target=self.worldwide_fixed, daemon=True),
            Thread(target=self.auto_anishexploits_fixed, daemon=True)
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join(timeout=300)
        
        # Generate final PDF
        self.generate_target_pdf()

def main():
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: python3 osint_v85.py <target>")
        print(f"{Fore.CYAN}Ex: python3 osint_v85.py 9876543210")
        print(f"{Fore.CYAN}Ex: python3 osint_v85.py john@example.com")
        sys.exit(1)
    
    osint = UltimateOSINTv85()
    osint.target = sys.argv[1]
    osint.ultimate_scan_v85()

if __name__ == "__main__":
    main()
```

