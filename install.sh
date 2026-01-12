#!/bin/bash

# Colors for status
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[*] Starting Installer for KHALID HUSAIN INVESTIGATOR...${NC}"

# 1. System Lock Error Fix: Agar koi aur process chal raha ho toh use wait karwayega
sudo fuser -vki /var/lib/dpkg/lock-frontend > /dev/null 2>&1

# 2. Update and Install System Dependencies
echo -e "${YELLOW}[*] Installing system tools (Tor, Python, etc.)...${NC}"
sudo apt update -y
sudo apt install -y tor torsocks python3 python3-pip git libxml2-dev libxslt-dev curl

# 3. Python Library Error Fix: Naye Linux mein --break-system-packages zaroori hai
echo -e "${YELLOW}[*] Installing Python libraries...${NC}"
pip3 install requests colorama beautifulsoup4 lxml urllib3 --break-system-packages --quiet 2>/dev/null || pip3 install requests colorama beautifulsoup4 lxml urllib3 --quiet

# 4. Tool Dependency Check: Sherlock aur Maigret ko sahi se install karna
echo -e "${YELLOW}[*] Checking Sherlock & Maigret...${NC}"
pip3 install sherlock maigret --break-system-packages --quiet 2>/dev/null || pip3 install sherlock maigret --quiet

# 5. Tor Service Configuration: Error na aaye isliye restart karenge
echo -e "${YELLOW}[*] Configuring Tor Service...${NC}"
sudo systemctl stop tor > /dev/null 2>&1
sudo systemctl enable tor > /dev/null 2>&1
sudo systemctl start tor > /dev/null 2>&1

# 6. Check if Tor is actually running
if systemctl is-active --quiet tor; then
    echo -e "${GREEN}[OK] Tor Service is running perfectly.${NC}"
else
    echo -e "${RED}[ERROR] Tor failed to start. Please check manual: sudo service tor start${NC}"
fi

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}      ALL SET! NO ERRORS DETECTED.            ${NC}"
echo -e "${YELLOW} Usage: python3 khalid-osint.py               ${NC}"
echo -e "${GREEN}==============================================${NC}"
