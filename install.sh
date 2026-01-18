#!/bin/bash

# --- SETTINGS ---
REPO_URL="https://github.com/Khalidhusain786/osint.git"
INSTALL_DIR="/home/kali/osint"

# Colors
CYAN='\033[0-36m'
GREEN='\033[0-32m'
RED='\033[0-31m'
NC='\033[0m'

echo -e "${CYAN}[*] KHALID OSINT - FULL AUTOMATION STARTING...${NC}"

# 1. System Dependencies
echo -e "${GREEN}[+] Installing System Dependencies...${NC}"
sudo apt update -y
sudo apt install -y python3-pip tor git curl python3-venv
sudo service tor start

# 2. Tor Control Port Configuration (For Circuit Rotation)
echo -e "${GREEN}[+] Configuring Tor Control Port...${NC}"
if ! grep -q "ControlPort 9051" /etc/tor/torrc; then
    echo "ControlPort 9051" | sudo tee -a /etc/tor/torrc
    echo "CookieAuthentication 0" | sudo tee -a /etc/tor/torrc
    sudo service tor restart
fi

# 3. Cleanup and Clone
echo -e "${GREEN}[+] Fresh Cloning Repository...${NC}"
sudo rm -rf "$INSTALL_DIR"
git clone "$REPO_URL" "$INSTALL_DIR"
cd "$INSTALL_DIR" || exit

# 4. Python Environment & Library Setup
echo -e "${GREEN}[+] Installing Python Libraries...${NC}"
# Breaking system packages fix for Kali
pip3 install aiohttp playwright stem folium streamlit pyvis pandas --break-system-packages 2>/dev/null

# 5. Playwright Browser Install (Crucial for Stealth Scrape)
echo -e "${GREEN}[+] Installing Playwright Browsers...${NC}"
python3 -m playwright install chromium
python3 -m playwright install-deps

# 6. AUTO-FIX: khalid-osint.py (Indentation & Missing Variables)
echo -e "${GREEN}[+] Patching khalid-osint.py for errors...${NC}"

# Aisa code jo missing variable aur indentation theek karega
cat << 'EOF' > khalid-osint.py
import asyncio
import aiohttp
from playwright.async_api import async_playwright
import stem.control
from stem import Signal
import random
import re
import json
import os

REAL_ONION_MARKETS = ["http://torchde9u7y3j.onion", "http://danwin1210.onion"]
MARIANA_DEEP_WEB = ["http://marianaonionxxx.onion", "http://deepwebmariana.onion"]
ALL_ONION_MARKETS = REAL_ONION_MARKETS + MARIANA_DEEP_WEB

class EliteOnionCollector:
    def __init__(self, target):
        self.target = target
        self.found_items = {'vendors': [], 'drops': [], 'wallets': [], 'emails': [], 'phones': [], 'domains': []}
        self.wallets, self.emails, self.phones, self.domains, self.drops = [], [], [], [], []

    async def init_tor_rotation(self):
        try:
            self.controller = stem.control.Controller.from_port(port=9051)
            self.controller.authenticate()
        except:
            print("⚠️ Tor Control Port Error")

    async def stealth_scrape(self, url):
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True, proxy={'server': 'socks5://127.0.0.1:9050'})
                page = await browser.new_page()
                await page.goto(url, timeout=60000)
                html = await page.content()
                await browser.close()
                return html
            except:
                return None

    def extract_all_iocs(self, html):
        patterns = {
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'btc': r'(?:bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}',
            'vendors': r'(?:vendor|seller)[\s:]*([A-Za-z0-9\s\-_]{3,20})'
        }
        return {k: re.findall(v, html, re.I) for k, v in patterns.items()}

    async def collect_all(self):
        await self.init_tor_rotation()
        for market in ALL_ONION_MARKETS[:3]:
            print(f"🔍 Scanning: {market}")
            html = await self.stealth_scrape(market)
            if html:
                iocs = self.extract_all_iocs(html)
                print(f"   Found: {len(iocs.get('emails', []))} emails")

async def main():
    print("💎 ELITE MARIANA COLLECTOR v6.0")
    target = input("🎯 Target Name: ")
    os.makedirs("iocs", exist_ok=True)
    c = EliteOnionCollector(target)
    await c.collect_all()

if __name__ == "__main__":
    asyncio.run(main())
EOF

# 7. Final Execution
echo -e "${GREEN}[✔] SETUP COMPLETE! STARTING TOOL...${NC}"
sleep 2
clear
python3 khalid-osint.py
