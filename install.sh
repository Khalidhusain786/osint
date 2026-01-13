#!/bin/bash

# Visual Styling
G='\033[0;32m'
R='\033[0;31m'
C='\033[0;36m'
NC='\033[0m'

echo -e "${C}[*] Khalid Hybrid OSINT: Universal Auto-Fixer (Kali & Termux)...${NC}"

# 1. Platform Detection & Tool Installation
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    echo -e "${G}[+] Termux Detected. Updating packages...${NC}"
    pkg update -y && pkg upgrade -y
    pkg install python git tor libxml2 libxslt clang make -y
    BIN_DIR="/data/data/com.termux/files/usr/bin"
    PIP_CMD="pip install"
    # Start Tor for Termux
    pkill tor
    tor > /dev/null 2>&1 &
else
    echo -e "${G}[+] Linux/Kali Detected. Updating packages...${NC}"
    sudo apt update -qq
    sudo apt install -y python3-pip tor torsocks sherlock libxml2-dev libxslt-dev -y
    BIN_DIR="/usr/local/bin"
    PIP_CMD="sudo pip install --break-system-packages"
    # Start Tor for Kali
    sudo service tor restart
fi

# 2. Python Dependencies & Tools
echo -e "${G}[+] Installing Maigret, Sherlock & Libraries...${NC}"
$PIP_CMD --upgrade pip
$PIP_CMD requests[socks] colorama beautifulsoup4 lxml urllib3 maigret sherlock --no-cache-dir

# 3. THE PERMANENT FIX: Symbolic Linking
# Isse 'maigret' aur 'sherlock' command global ho jayenge (No more Skipping error)
echo -e "${G}[+] Linking tools to system path permanently...${NC}"
M_PATH=$(which maigret || find $HOME -name maigret | grep bin | head -n 1)
S_PATH=$(which sherlock || find $HOME -name sherlock | grep bin | head -n 1)

if [ ! -z "$M_PATH" ]; then ln -sf "$M_PATH" "$BIN_DIR/maigret"; fi
if [ ! -z "$S_PATH" ]; then ln -sf "$S_PATH" "$BIN_DIR/sherlock"; fi

# 4. Final Setup
chmod +x khalid-osint.py
mkdir -p reports

echo -e "${C}----------------------------------------------------${NC}"
echo -e "${G}[SUCCESS] Setup complete! Sherlock & Maigret are now ACTIVE.${NC}"
echo -e "${G}[➔] Run: python3 khalid-osint.py${NC}"
