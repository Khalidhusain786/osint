#!/bin/bash

# Visual Styling
G='\033[0;32m'
R='\033[0;31m'
C='\033[0;36m'
NC='\033[0m'

echo -e "${C}[*] Khalid Husain OSINT: Auto-Fix & Fast Setup Mode...${NC}"

# PROBLEM 1: Wrong File Name (Auto-Rename)
if [ -f "khalid-osint.py" ]; then
    echo -e "${G}[FIX] Renaming khalid-osint.py to main.py...${NC}"
    mv khalid-osint.py main.py
fi

# PROBLEM 2: Missing System Tools (Fast Install, No Upgrade)
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    echo -e "${G}[+] Termux Detected. Installing core deps...${NC}"
    pkg install python git tor clang make libxml2 libxslt -y > /dev/null 2>&1
    # Auto-start Tor for Termux
    pkill tor
    tor > /dev/null 2>&1 &
else
    echo -e "${G}[+] Kali Linux Detected. Installing core deps...${NC}"
    sudo apt update -qq
    sudo apt install -y python3-pip tor torsocks libxml2-dev libxslt-dev > /dev/null 2>&1
    # Auto-start Tor for Kali
    sudo service tor restart > /dev/null 2>&1
fi

# PROBLEM 3: Python Libraries Errors
echo -e "${C}[*] Solving Python dependencies...${NC}"
pip install --no-cache-dir --upgrade pip > /dev/null 2>&1
pip install --no-cache-dir requests[socks] colorama beautifulsoup4 lxml urllib3 > /dev/null 2>&1

# PROBLEM 4: Directory Permissions
mkdir -p reports
chmod +x *

# FINAL AUTO-START
clear
echo -e "${G}[SUCCESS] Everything Fixed. Starting Tool...${NC}"
python3 main.py
