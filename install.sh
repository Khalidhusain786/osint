#!/bin/bash

# Visual Colors
G='\033[0;32m'
R='\033[0;31m'
C='\033[0;36m'
NC='\033[0m'

echo -e "${C}[*] Khalid Husain OSINT: Fixing Maigret & Sherlock Paths...${NC}"

# 1. Root Check
if [[ $EUID -ne 0 ]]; then
   echo -e "${R}[!] Please run as sudo: sudo ./install.sh${NC}"
   exit 1
fi

# 2. Update and Install Core Tools
apt update -qq
apt install -y python3-pip tor torsocks sherlock libxml2-dev libxslt-dev -y

# 3. Maigret & Libraries Installation
echo -e "${G}[+] Installing Maigret and Dependencies...${NC}"
pip install --break-system-packages --upgrade pip
pip install --break-system-packages requests[socks] colorama beautifulsoup4 lxml urllib3 maigret --no-cache-dir

# 4. THE PERMANENT FIX: Linking paths to /usr/bin
# Isse aapka Python script 'maigret' command ko turant dhoond lega
echo -e "${G}[+] Creating Permanent System Links...${NC}"
M_PATH=$(which maigret || echo "$HOME/.local/bin/maigret")
S_PATH=$(which sherlock || echo "$HOME/.local/bin/sherlock")

ln -sf "$M_PATH" /usr/bin/maigret
ln -sf "$S_PATH" /usr/bin/sherlock
ln -sf "$M_PATH" /usr/local/bin/maigret
ln -sf "$S_PATH" /usr/local/bin/sherlock

# 5. Service Start
systemctl restart tor
chmod +x khalid-osint.py
mkdir -p reports

echo -e "${G}[SUCCESS] Paths Fixed. Now run: python3 khalid-osint.py${NC}"
