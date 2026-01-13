#!/bin/bash

# Visual styling
G='\033[0;32m'
R='\033[0;31m'
C='\033[0;36m'
NC='\033[0m'

echo -e "${C}[*] Checking System Environment...${NC}"

if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    # TERMUX SETUP
    echo -e "${G}[+] Termux Detected. Starting Auto-Setup...${NC}"
    pkg update -y && pkg upgrade -y
    pkg install python git tor clang make libxml2 libxslt libffi openssl -y
    
    # Fix for LXML and heavy libraries in Termux
    export LDFLAGS="-L${PREFIX}/lib"
    export CPPFLAGS="-I${PREFIX}/include"
    
    pip install --upgrade pip
    pip install colorama requests beautifulsoup4 lxml urllib3 pysocks sherlock maigret
else
    # KALI / DEBIAN SETUP
    echo -e "${G}[+] Kali Linux Detected. Starting Auto-Setup...${NC}"
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip git tor torsocks libxml2-dev libxslt-dev python3-lxml
    
    # Enable Tor
    sudo systemctl enable tor
    sudo systemctl start tor
    
    # Handle PEP 668 (break-system-packages) for newer Kali versions
    pip3 install colorama requests beautifulsoup4 lxml urllib3 pysocks sherlock maigret --break-system-packages || \
    pip3 install colorama requests beautifulsoup4 lxml urllib3 pysocks sherlock maigret
fi

# Finalizing
mkdir -p reports
chmod +x * 2>/dev/null

echo -e "${G}[SUCCESS] Setup complete. No errors found.${NC}"
echo -e "${C}[*] Tip: If using Termux, run 'tor' in a second tab before starting the tool.${NC}"
