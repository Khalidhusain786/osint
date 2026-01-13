#!/bin/bash
# Colors
G='\033[0;32m'
R='\033[0;31m'
C='\033[0;36m'
NC='\033[0m'

echo -e "${C}[*] System Scan & Setup Start Ho Raha Hai...${NC}"

# Check for Termux
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    echo -e "${G}[+] Termux Detected. Installing optimized packages...${NC}"
    pkg update -y && pkg upgrade -y
    # Important: Termux mein 'binutils' aur 'rust' zaroori hain latest python packages ke liye
    pkg install python git tor clang make libxml2 libxslt libffi openssl libcrypt rust binutils -y
    
    pip install --upgrade pip
    pip install colorama requests beautifulsoup4 lxml urllib3[socks] pysocks sherlock maigret
else
    # Kali / Debian Setup
    echo -e "${G}[+] Kali/Linux Detected. Fixing Permissions...${NC}"
    sudo apt-get update
    # Essential build tools for Python C-extensions
    sudo apt-get install -y python3 python3-pip python3-dev git tor torsocks \
    libxml2-dev libxslt-dev build-essential libssl-dev libffi-dev

    # Tor Service fix
    sudo systemctl enable tor
    sudo systemctl start tor
    
    # Python package fix (PEP 668)
    pip3 install colorama requests beautifulsoup4 lxml urllib3[socks] pysocks sherlock maigret --break-system-packages
fi

mkdir -p reports
chmod +x * 2>/dev/null
echo -e "${G}[SUCCESS] Setup Complete. Ab aap tool run kar sakte hain.${NC}"
