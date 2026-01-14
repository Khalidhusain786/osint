#!/bin/bash

# --- KHALID HUSAIN PENTEST PRO v84.0 INSTALLER ---
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}--- Starting Khalid Pentest Pro Installation ---${NC}"

# 1. Update System
echo -e "${GREEN}[+] Updating system packages...${NC}"
sudo apt-get update -y

# 2. Install System Dependencies (Kali/Debian/Ubuntu)
echo -e "${GREEN}[+] Installing system binaries (Tor, Subfinder, etc.)...${NC}"
sudo apt-get install -y python3-pip tor torsocks nmap subfinder amass theharvester dnsrecon libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

# 3. Setup Tor
echo -e "${GREEN}[+] Enabling Tor service...${NC}"
sudo systemctl enable tor
sudo systemctl start tor

# 4. Install Python Dependencies
echo -e "${GREEN}[+] Installing Python libraries...${NC}"
pip3 install --upgrade pip
pip3 install aiohttp colorama weasyprint

# 5. Set Permissions
echo -e "${GREEN}[+] Setting executable permissions...${NC}"
chmod +x khalid-osint.py

echo -e "${RED}══════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}    KHALID HUSAIN PENTEST PRO v84.0 INSTALLED${NC}"
echo -e "${GREEN}    Usage: python3 khalid-osint.py <target>${NC}"
echo -e "${RED}══════════════════════════════════════════════════════${NC}"
