#!/bin/bash
# Visual Colors
G='\033[0;32m'
C='\033[0;36m'
NC='\033[0m'

echo -e "${C}[*] Khalid Husain OSINT: Fixing Maigret & Sherlock Paths Permanently...${NC}"

# 1. Necessary Packages
sudo apt update -qq
sudo apt install -y python3-pip tor torsocks sherlock libxml2-dev libxslt-dev -y

# 2. Maigret Installation
echo -e "${G}[+] Installing Maigret via PIP...${NC}"
pip install maigret --break-system-packages --no-cache-dir

# 3. PERMANENT LINKING (Yeh sabse important step hai)
# Isse system ko 'maigret' command ka pata chal jayega
M_PATH=$(which maigret || echo "$HOME/.local/bin/maigret")
sudo ln -sf "$M_PATH" /usr/local/bin/maigret

S_PATH=$(which sherlock || echo "$HOME/.local/bin/sherlock")
sudo ln -sf "$S_PATH" /usr/local/bin/sherlock

# 4. Permissions & Tor
sudo service tor restart
chmod +x khalid-osint.py
mkdir -p reports

echo -e "${G}[SUCCESS] System paths synchronized. Run your script now.${NC}"
