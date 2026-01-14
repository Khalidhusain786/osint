#!/bin/bash
# 🔥 KHALID HUSAIN RAW PRO v86.0 INSTALLER 🔥

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}--- [!] Khalid Engine: Auto-Fixing Dependencies ---${NC}"

# 1. Update Repo
sudo apt-get update -y

# 2. Fix Chromium & Driver (Commonly missing in Kali)
echo -e "${YELLOW}[+] Fixing Chromium & Selenium Drivers...${NC}"
sudo apt-get install -y chromium chromium-driver || sudo apt-get install -y chromium-browser chromium-chromedriver

# 3. System Binaries for PDF and Network
echo -e "${YELLOW}[+] Installing System Libs...${NC}"
sudo apt-get install -y tor torsocks nmap subfinder amass theharvester dnsrecon \
python3-pip libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libjpeg-dev libopenjp2-7-dev

# 4. Python Libraries (Force Reinstall for Stability)
echo -e "${YELLOW}[+] Installing Python Modules...${NC}"
pip3 install --upgrade pip
pip3 install --force-reinstall aiohttp colorama weasyprint selenium webdriver-manager

# 5. Syntax Cleaning (Fixes the ```python error)
if [ -f "khalid_raw_v86.py" ]; then
    sed -i '/^```/d' khalid_raw_v86.py
    chmod +x khalid_raw_v86.py
fi

# 6. Tor Service
sudo service tor restart

echo -e "\n${GREEN}✔ ALL TOOLS FIXED & UPDATED${NC}"
echo -e "${CYAN}Command: python3 khalid_raw_v86.py <phone>${NC}"
