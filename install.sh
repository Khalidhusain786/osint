#!/bin/bash

# --- KHALID OSINT v83.0 AUTO-FIXER & INSTALLER ---
# Professional, No Lags, Auto-Repair

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}--- [!] Khalid Ultimate Engine: Fixing Environment ---${NC}"

# 1. Update Package List (No Full Upgrade to save time/space)
echo -e "${YELLOW}[1/5] Updating Repository Lists...${NC}"
sudo apt-get update -y

# 2. Install System Dependencies (Crucial for WeasyPrint & PDF)
echo -e "${YELLOW}[2/5] Installing PDF & Graphics Engines...${NC}"
sudo apt-get install -y python3-pip python3-dev \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b \
    libjpeg-dev libopenjp2-7-dev libffi-dev \
    curl git tor torsocks nmap -q

# 3. Install Kali Recon Tools (If missing)
echo -e "${YELLOW}[3/5] Checking Kali Recon Suite...${NC}"
TOOLS=(subfinder amass theHarvester dnsrecon dnsenum holehe)
for tool in "${TOOLS[@]}"; do
    if ! command -v $tool &> /dev/null; then
        echo -e "${CYAN}   [+] Installing $tool...${NC}"
        sudo apt-get install -y $tool -q
    else
        echo -e "${GREEN}   [✔] $tool already installed.${NC}"
    fi
done

# 4. Fix Python Environment & Libraries
echo -e "${YELLOW}[4/5] Fixing Python Dependencies (Auto-Repair)...${NC}"
# Use --force-reinstall only for core libs to fix broken links
pip3 install --upgrade pip
pip3 install colorama requests beautifulsoup4 markdown weasyprint --quiet

# Fix for Sherlock & Maigret pathing
pip3 install sherlock maigret socialscan --quiet

# 5. Syntax & Permission Auto-Fix
echo -e "${YELLOW}[5/5] Applying Final Permissions...${NC}"
SCRIPT_NAME="pentest_v83.py" # Apni file ka naam yahan check karein
if [ -f "$SCRIPT_NAME" ]; then
    sed -i '/^```/d' "$SCRIPT_NAME" # Deletes any markdown backticks
    chmod +x "$SCRIPT_NAME"
    echo -e "${GREEN}[✔] $SCRIPT_NAME is ready.${NC}"
else
    echo -e "${RED}[✘] Error: $SCRIPT_NAME not found!${NC}"
fi

# Tor Service Sync
sudo service tor restart

echo -e "\n${RED}======================================================"
echo -e "${YELLOW}       KHALID OSINT v83.0 - SETUP COMPLETE"
echo -e "${GREEN}    Command: python3 $SCRIPT_NAME <target>"
echo -e "${RED}======================================================${NC}"
