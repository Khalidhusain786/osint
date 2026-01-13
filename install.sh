#!/bin/bash

# Rangon ka setup
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}--------------------------------------------------${NC}"
echo -e "${GREEN}    KHALID OSINT - FORENSIC ENVIRONMENT FIXER     ${NC}"
echo -e "${CYAN}--------------------------------------------------${NC}"

# 1. System Level Fixes (Kail/Debian specific)
echo -e "${YELLOW}[*] Fixing System Dependencies...${NC}"
sudo apt-get update -y
sudo apt-get install -y python3-full python3-pip tor torsocks \
    libxml2-dev libxslt-dev zlib1g-dev libpcap-dev \
    build-essential python3-dev -y

# 2. Tor Connection Fix
echo -e "${YELLOW}[*] Restarting Ghost Tunnel (Tor)...${NC}"
sudo systemctl stop tor
sudo systemctl start tor
sudo systemctl enable tor

# 3. Python Dependency Force Install
# '--break-system-packages' Kali Linux ke naye versions ke liye zaroori hai
echo -e "${YELLOW}[*] Installing Python Modules (Force Mode)...${NC}"
python3 -m pip install --upgrade pip --break-system-packages
python3 -m pip install wheel setuptools --break-system-packages

echo -e "${YELLOW}[*] Compiling LXML and OSINT Modules...${NC}"
python3 -m pip install colorama requests beautifulsoup4 lxml fpdf reportlab urllib3 \
    sherlock maigret --break-system-packages

# 4. Binary Path Fix (Subprocess errors ko rokne ke liye)
echo -e "${YELLOW}[*] Linking Tool Binaries...${NC}"
sudo ln -sf /home/$(whoami)/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf /home/$(whoami)/.local/bin/maigret /usr/local/bin/maigret

# 5. Permission & Reports setup
mkdir -p reports
chmod +x *.py

echo -e "${CYAN}--------------------------------------------------${NC}"
echo -e "${GREEN}[✓] INSTALLATION SUCCESSFUL!${NC}"
echo -e "${YELLOW}[!] Status Check: Tor is $(systemctl is-active tor)${NC}"
echo -e "${GREEN}[>] Run command: python3 khalid-osint.py 'target'${NC}"
echo -e "${CYAN}--------------------------------------------------${NC}"
