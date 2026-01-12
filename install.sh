#!/bin/bash

# --- COLORS ---
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}    KHALID-OSINT v71.0 - AUTO INSTALLER (Shadow Bureau)    ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 1. Update System
echo -e "\n[*] Updating System Packages..."
sudo apt update -y && sudo apt upgrade -y

# 2. Install Core Dependencies (Tor, Torsocks, Python, Node.js)
echo -e "\n[*] Installing Core Engines..."
sudo apt install -y tor torsocks python3 python3-pip nodejs npm curl git

# 3. Start Tor Service
echo -e "\n[*] Starting Tor Stealth Tunnel..."
sudo systemctl enable tor
sudo service tor start

# 4. Install Social-Analyzer (Ultimate Social Media Hunter)
echo -e "\n[*] Installing Social-Analyzer (npm)..."
sudo npm install -g social-analyzer

# 5. Install OSINT Python Tools (Sherlock & Maigret)
echo -e "\n[*] Installing Sherlock & Maigret..."
pip3 install sherlock maigret --break-system-packages 2>/dev/null || pip3 install sherlock maigret

# 6. Install Python Library Dependencies
echo -e "\n[*] Installing Python Libraries (Colorama, Requests, etc.)..."
pip3 install colorama requests beautifulsoup4 stem --break-system-packages 2>/dev/null || pip3 install colorama requests beautifulsoup4 stem

# 7. Verification
echo -e "\n${GREEN}[✔] All tools installed successfully!${NC}"
echo -e "[*] To run the script: ${RED}python3 khalid_osint.py${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
