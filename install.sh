#!/bin/bash
# 🔥 KHALID HUSAIN BULLETPROOF AUTO-FIXER v86.2 🔥

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}[!] Starting Zero-Error Repair Engine...${NC}"

# 1. Repo aur System Update
sudo apt-get update -y

# 2. Syntax Repair (Fixes line 306 & Emojis)
if [ -f "khalid-osint.py" ]; then
    echo -e "${GREEN}[+] Auto-Fixing Syntax Errors & Emojis...${NC}"
    # Sabhi emojis aur prose text lines ke aage '#' lagana taaki Python error na de
    sed -i '/🔍/s/^/# /' khalid-osint.py
    sed -i '/⚔️/s/^/# /' khalid-osint.py
    sed -i '/🔥/s/^/# /' khalid-osint.py
    sed -i '/^```/d' khalid-osint.py # Triple backticks hatao
    chmod +x khalid-osint.py
fi

# 3. Essential Tools Installation
echo -e "${GREEN}[+] Installing All OSINT Tools...${NC}"
tools=(nmap subfinder amass theharvester dnsrecon dnsenum tor torsocks python3-pip chromium-driver)
for tool in "${tools[@]}"; do
    sudo apt-get install -y $tool -q
done

# 4. Python Library Force-Sync
echo -e "${GREEN}[+] Syncing Python Libraries...${NC}"
pip3 install --upgrade pip --quiet
pip3 install colorama requests beautifulsoup4 markdown weasyprint selenium webdriver-manager aiohttp --quiet

# 5. Service Refresh
sudo service tor restart

echo -e "\n${RED}=========================================="
echo -e "${GREEN}      SAB KUCH FIX HO GAYA HAI! RUN NOW."
echo -e "${RED}==========================================${NC}"
