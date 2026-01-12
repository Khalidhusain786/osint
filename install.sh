#!/bin/bash

# --- Colors for Output ---
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================${NC}"
echo -e "${GREEN}    KHALID-OSINT v58.0 - AUTO INSTALLER SYSTEM      ${NC}"
echo -e "${BLUE}====================================================${NC}"

# 1. Check Root Privileges
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[!] Please run as root (use sudo ./install.sh)${NC}"
   exit 1
fi

# 2. Update System
echo -e "${BLUE}[*] Updating system repositories...${NC}"
apt update -y && apt upgrade -y

# 3. Install Essential Core Tools
echo -e "${BLUE}[*] Installing Core Recon Tools (Amass, Shodan, Tor)...${NC}"
apt install -y python3 python3-pip tor curl git amass theharvester sherlock shodan

# 4. Install Maigret & Python Dependencies
echo -e "${BLUE}[*] Installing Python OSINT Libraries...${NC}"
pip3 install --upgrade pip
pip3 install requests colorama maigret

# 5. Fix for WhatsMyName (Clone if not exists)
if [ ! -d "WhatsMyName" ]; then
    echo -e "${BLUE}[*] Cloning WhatsMyName Repository...${NC}"
    git clone https://github.com/WebBreacher/WhatsMyName.git
    cd WhatsMyName && pip3 install -r requirements.txt && cd ..
fi

# 6. Setup TOR Service
echo -e "${BLUE}[*] Enabling TOR Service...${NC}"
systemctl enable tor
systemctl start tor

# 7. Final Verification
echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}[OK] All Heavy Tools Installed Successfully!        ${NC}"
echo -e "${BLUE}    - Sherlock: Installed                           ${NC}"
echo -e "${BLUE}    - Maigret: Installed                            ${NC}"
echo -e "${BLUE}    - Amass: Installed                              ${NC}"
echo -e "${BLUE}    - theHarvester: Installed                       ${NC}"
echo -e "${BLUE}    - Shodan CLI: Installed                         ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}Run the tool using: python3 khalid_osint.py         ${NC}"
