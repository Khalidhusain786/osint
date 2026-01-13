#!/bin/bash

# Visual Styling
G='\033[0;32m'
R='\033[0;31m'
C='\033[0;36m'
NC='\033[0m'

echo -e "${C}[*] Khalid Husain OSINT: Auto-Fix & Fast Setup Mode...${NC}"

# 1. Rename File (Consistent with main script)
if [ -f "khalid-osint.py" ]; then
    echo -e "${G}[FIX] Renaming to main.py...${NC}"
    mv khalid-osint.py main.py
fi

# 2. Install Core Dependencies
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    echo -e "${G}[+] Termux Detected...${NC}"
    pkg install python git tor clang make libxml2 libxslt -y
    # Install Sherlock & Maigret for Termux
    pip install sherlock maigret --no-cache-dir
    tor > /dev/null 2>&1 &
else
    echo -e "${G}[+] Kali/Linux Detected...${NC}"
    sudo apt update -qq
    sudo apt install -y python3-pip tor torsocks sherlock libxml2-dev libxslt-dev -y
    # Install Maigret via pip (Kali repo me nahi hota aksar)
    pip install maigret --break-system-packages --no-cache-dir
    sudo service tor restart
fi

# 3. Python Libraries
echo -e "${C}[*] Installing Python dependencies...${NC}"
pip install --no-cache-dir requests[socks] colorama beautifulsoup4 lxml urllib3 --break-system-packages

# 4. Final Permissions
mkdir -p reports
chmod +x main.py

clear
echo -e "${G}[SUCCESS] Sherlock, Maigret, and Tor are ready! Starting Tool...${NC}"
python3 main.py
