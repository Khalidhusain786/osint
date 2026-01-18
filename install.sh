#!/usr/bin/env bash

set -euo pipefail

echo ""
echo "================================================================"
echo "     KHALID HUSAIN ELITE MARIANA COLLECTOR - INSTALLER v1.0    "
echo "================================================================"
echo ""

echo "[+] Updating Kali packages ..."
sudo apt update -y && sudo apt upgrade -y

echo ""
echo "[+] Installing base dependencies ..."
sudo apt install -y \
    python3 python3-pip python3-venv git curl wget unzip tor \
    libnss3 libatk-bridge2.0-0 libxkbcommon0 libgbm1 libasound2 \
    libxshmfence1 libdrm2 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 libatk1.0-0 libatk-bridge2.0-0 \
    libgtk-3-0 libgdk-pixbuf-2.0-0

echo ""
echo "[+] Installing Tor Browser dependencies & stem ..."
sudo apt install -y torbrowser-launcher python3-stem

echo ""
echo "[+] Starting & enabling Tor service ..."
sudo systemctl enable tor
sudo systemctl restart tor

echo ""
echo "[+] Installing Python packages (requirements) ..."
pip3 install --upgrade pip wheel setuptools
pip3 install --user --break-system-packages \
    aiohttp playwright stem requests pandas folium streamlit pyvis \
    beautifulsoup4 lxml fake-useragent

echo ""
echo "[+] Installing Playwright browsers (chromium + firefox) ..."
playwright install chromium firefox --with-deps --no-shell

echo ""
echo "[+] Creating Tor control authentication (if needed) ..."
# Minimal torrc configuration for stem control (port 9051)
if ! grep -q "ControlPort 9051" /etc/tor/torrc; then
    echo "" | sudo tee -a /etc/tor/torrc
    echo "ControlPort 9051" | sudo tee -a /etc/tor/torrc
    echo "CookieAuthentication 1" | sudo tee -a /etc/tor/torrc
    sudo systemctl restart tor
fi

echo ""
echo "[+] Creating iocs folder (if not exists) ..."
mkdir -p ~/iocs

echo ""
echo "[+] Installation finished."
echo ""
echo "Run commands:"
echo ""
echo "    cd ~/Desktop   # or wherever you want"
echo "    git clone https://github.com/Khalidhusain786/osint.git   # if repo exists"
echo "    cd osint"
echo "    python3 khalid-osint.py 7696408248"
echo ""
echo "Or one-liner (after git clone):"
echo "    cd osint && python3 khalid-osint.py 7696408248"
echo ""
echo "Note:"
echo "  • If you see 'stem' authentication error → check /etc/tor/torrc"
echo "  • If Playwright fails → run:   playwright install --with-deps"
echo "  • Tor must be running:   sudo service tor status"
echo ""
echo "================================================================"
echo ""

exit 0
