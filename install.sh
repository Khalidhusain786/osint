#!/bin/bash
# 🔥 KHALID HUSAIN AUTO-FIXER & INSTALLER v83.1 🔥

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}[!] Starting Khalid Engine Repair...${NC}"

# 1. Python Syntax Repair (Sabse Important)
# Ye command line 308 jaise plain text errors aur backticks ko remove karega
if [ -f "khalid-osint.py" ]; then
    echo -e "${GREEN}[+] Repairing Python Syntax Errors...${NC}"
    sed -i '/^```/d' khalid-osint.py # Markdown hatao
    sed -i '/⚔️/s/^/# /' khalid-osint.py # Emoji lines ko comment banao
    chmod +x khalid-osint.py
fi

# 2. Dependency Installation
echo -e "${GREEN}[+] Installing Missing Tools...${NC}"
sudo apt-get update -y
sudo apt-get install -y nmap subfinder amass theharvester dnsrecon dnsenum \
python3-pip libpango-1.0-0 libharfbuzz0b tor torsocks -q

# 3. Python Library Fix
echo -e "${GREEN}[+] Syncing Python Modules...${NC}"
pip3 install colorama requests beautifulsoup4 markdown weasyprint --quiet

# 4. Service Restart
sudo service tor restart

echo -e "\n${RED}=========================================="
echo -e "${GREEN}      ALL ERRORS FIXED! RUN NOW."
echo -e "${RED}==========================================${NC}"
