#!/bin/bash

# Fast color codes
G='\e[1;32m'
B='\e[1;34m'
R='\e[1;31m'
N='\e[0m'

echo -e "${B}[*] Khalid Husain OSINT - Fast Setup Starting...${N}"

# Check environment (Kali or Termux) and install only missing core deps
if [ -f /usr/bin/apt ]; then
    # Kali Linux: Silent install zaroori libraries
    sudo apt update -qq
    sudo apt install -y python3-pip tor torsocks libxml2-dev libxslt-dev > /dev/null 2>&1
elif [ -f /usr/bin/pkg ]; then
    # Termux: Silent install
    pkg install -y python tor libxml2 libxslt clang make > /dev/null 2>&1
fi

# Install Python requirements silently
echo -e "${G}[*] Installing Python Dependencies...${N}"
pip install --no-cache-dir requests[socks] colorama beautifulsoup4 lxml urllib3 > /dev/null 2>&1

# Setup Reports Directory
mkdir -p reports

# Start Tor Service (Background)
echo -e "${G}[*] Activating Ghost Tunnel (Tor)...${N}"
if [ -f /usr/bin/apt ]; then
    sudo service tor start > /dev/null 2>&1
else
    tor > /dev/null 2>&1 &
fi

# Permissions fix
chmod +x *

# Auto-Start the Tool
echo -e "${B}[OK] Setup Complete. Launching Investigator...${N}"
sleep 2
clear
python3 main.py
