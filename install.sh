#!/bin/bash

# --- KHALID HUSAIN PENTEST PRO v84.0 AUTO-ENGINE ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}--- [!] Khalid Engine: Auto-Fixing & Installing Tools ---${NC}"

# Function to install/update without upgrading the whole system
auto_tool() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${YELLOW}[+] Installing $1...${NC}"
        sudo apt-get install -y $1
    else
        echo -e "${GREEN}[✔] Updating $1...${NC}"
        sudo apt-get install --only-upgrade -y $1 &> /dev/null || true
    fi
}

# 1. System Dependencies
echo -e "${CYAN}\n[1] Checking System Tools...${NC}"
sudo apt-get update -y # Only update package lists
tools=(tor torsocks nmap subfinder amass theharvester dnsrecon python3-pip curl git libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0)

for tool in "${tools[@]}"; do
    auto_tool $tool
done

# 2. Python Environment Fix (No Upgrade, Only Force Install)
echo -e "${CYAN}\n[2] Checking Python Libraries...${NC}"
pip3 install --force-reinstall aiohttp colorama weasyprint urllib3 2>/dev/null

# 3. Fixing Syntax Errors in Python Script (Auto-Remove Backticks)
echo -e "${CYAN}\n[3] Cleaning Python Script Syntax...${NC}"
if [ -f "khalid-osint.py" ]; then
    sed -i '/^```/d' khalid-osint.py
    chmod +x khalid-osint.py
    echo -e "${GREEN}[✔] Script cleaned and ready.${NC}"
fi

# 4. Service Repair
echo -e "${CYAN}\n[4] Starting Services...${NC}"
sudo service tor restart

echo -e "\n${RED}======================================================"
echo -e "${YELLOW}       KHALID OSINT ENGINE IS READY TO RUN"
echo -e "${RED}======================================================${NC}"
