#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}--- Khalid Hybrid OSINT Engine Installer ---${NC}"

# 1. Platform Detection
if [ -d "$HOME/.termux" ]; then
    PLATFORM="termux"
    echo -e "${YELLOW}[!] Platform Detected: Termux${NC}"
else
    PLATFORM="kali"
    echo -e "${YELLOW}[!] Platform Detected: Linux/Kali${NC}"
fi

# 2. Update and Basic Tools
echo -e "${GREEN}[*] Updating system packages...${NC}"
if [ "$PLATFORM" == "termux" ]; then
    pkg update -y && pkg upgrade -y
    pkg install -y python tor torsocks git clang make libxml2 libxslt
else
    sudo apt update -y
    sudo apt install -y python3 python3-pip tor torsocks git libxml2-dev libxslt-dev
fi

# 3. Python Dependencies
echo -e "${GREEN}[*] Installing Python libraries...${NC}"
pip install --upgrade pip
pip install colorama requests beautifulsoup4 lxml urllib3

# 4. Optional OSINT Tools (Sherlock & Maigret)
echo -e "${GREEN}[*] Setting up optional tools (Sherlock/Maigret)...${NC}"
pip install sherlock maigret 2>/dev/null || echo -e "${YELLOW}[!] Note: Maigret/Sherlock installation skipped or already present.${NC}"

# 5. Fix Tor Configuration (Termux specific)
if [ "$PLATFORM" == "termux" ]; then
    echo -e "${GREEN}[*] Configuring Tor for Termux...${NC}"
    # Ensure tor can run in background
    nohup tor > /dev/null 2>&1 &
fi

echo -e "${CYAN}---------------------------------------------${NC}"
echo -e "${GREEN}[SUCCESS] Installation Finished!${NC}"
echo -e "${YELLOW}Run the tool using: python khalid-osint.py${NC}"
