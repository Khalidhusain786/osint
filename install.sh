#!/bin/bash

# Colors for professional output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}--------------------------------------------------${NC}"
echo -e "${GREEN}    KHALID OSINT - INSTALLER & DEPENDENCY FIXER   ${NC}"
echo -e "${CYAN}--------------------------------------------------${NC}"

# 1. Update and System Dependencies
echo -e "${YELLOW}[*] Installing System Dependencies (Sudo required)...${NC}"
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip tor torsocks libxml2-dev libxslt-dev zlib1g-dev libpcap-dev

# 2. Fix Tor Configuration
echo -e "${YELLOW}[*] Configuring and Starting Tor Service...${NC}"
sudo systemctl enable tor
sudo systemctl start tor

# 3. Fix Python Environment & Libraries
echo -e "${YELLOW}[*] Installing Python Libraries...${NC}"
# lxml and beautifulsoup4 are critical for your clean_and_verify function
pip3 install --upgrade pip
pip3 install wheel setuptools
pip3 install colorama requests beautifulsoup4 lxml fpdf reportlab urllib3

# 4. Tool Specific Fixes (Sherlock/Maigret)
echo -e "${YELLOW}[*] Checking for OSINT Tools...${NC}"
if ! command -v sherlock &> /dev/null; then
    echo -e "${YELLOW}[!] Sherlock not found. Installing via pip...${NC}"
    pip3 install sherlock
fi

if ! command -v maigret &> /dev/null; then
    echo -e "${YELLOW}[!] Maigret not found. Installing via pip...${NC}"
    pip3 install maigret
fi

# 5. Directory Setup
echo -e "${YELLOW}[*] Finalizing Workspace...${NC}"
mkdir -p reports
chmod +x khalid-osint.py

echo -e "${CYAN}--------------------------------------------------${NC}"
echo -e "${GREEN}[✓] SUCCESS: Environment is ready.${NC}"
echo -e "${YELLOW}[!] Ensure Tor is running (Status: $(systemctl is-active tor))${NC}"
echo -e "${CYAN}--------------------------------------------------${NC}"
