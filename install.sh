#!/bin/bash

# Status Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}      KHALID HUSAIN - DIRECT INSTALLER        ${NC}"
echo -e "${GREEN}==============================================${NC}"

# 1. System Update & Lock Fix (Directly handles busy packages)
echo -e "${YELLOW}[*] Preparing system for HTTP/HTTPS/Onion access...${NC}"
sudo rm /var/lib/dpkg/lock-frontend > /dev/null 2>&1
sudo rm /var/lib/apt/lists/lock > /dev/null 2>&1
sudo apt update -y

# 2. Universal Dependencies (Adding lxml support specifically)
echo -e "${YELLOW}[*] Installing Core Tools...${NC}"
sudo apt install -y tor torsocks python3 python3-pip git libxml2-dev libxslt-dev curl python3-lxml

# 3. Python Library Force-Install (Bypassing OS restrictions)
echo -e "${YELLOW}[*] Installing Python Modules...${NC}"
# lxml, requests, aur bs4 ke bina code crash ho jayega, isliye inhe force install kiya hai
pip3 install requests colorama beautifulsoup4 lxml urllib3 --break-system-packages --quiet 2>/dev/null || \
pip3 install requests colorama beautifulsoup4 lxml urllib3 --quiet

# 4. OSINT Tools (Sherlock & Maigret)
echo -e "${YELLOW}[*] Installing Sherlock & Maigret for Registration Search...${NC}"
pip3 install sherlock maigret --break-system-packages --quiet 2>/dev/null || \
pip3 install sherlock maigret --quiet

# 5. Tor Service Direct Start
echo -e "${YELLOW}[*] Configuring Ghost Tunnel...${NC}"
sudo systemctl enable tor > /dev/null 2>&1
sudo systemctl restart tor > /dev/null 2>&1

# 6. Final Integrity Check
echo -e "${YELLOW}[*] Verification...${NC}"
if python3 -c "import lxml, requests, bs4, colorama" 2>/dev/null; then
    echo -e "${GREEN}[OK] All HTTP/HTTPS/Onion protocols ready.${NC}"
else
    echo -e "${RED}[!] Some modules failed. Retrying one last time...${NC}"
    sudo apt install -y python3-requests python3-bs4 python3-colorama
fi

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}       DIRECT INSTALLATION SUCCESSFUL         ${NC}"
echo -e "${YELLOW} Run Now: python3 khalid-osint.py             ${NC}"
echo -e "${GREEN}==============================================${NC}"
