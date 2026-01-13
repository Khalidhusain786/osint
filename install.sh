#!/bin/bash

# Visual Colors
G='\033[0;32m'
R='\033[0;31m'
C='\033[0;36m'
NC='\033[0m'

echo -e "${C}====================================================${NC}"
echo -e "${R}   KHALID HUSAIN OSINT - AUTO INSTALLER & FIXER     ${NC}"
echo -e "${C}====================================================${NC}"

# 1. Sudo check
if [[ $EUID -ne 0 ]]; then
   echo -e "${R}[!] Please run this script with sudo: sudo bash install.sh${NC}"
   exit 1
fi

# 2. System Dependencies
echo -e "${G}[*] Installing System Dependencies...${NC}"
apt update -qq
apt install -y python3-pip tor torsocks sherlock libxml2-dev libxslt-dev git -y

# 3. Python Libraries Fix
echo -e "${G}[*] Fixing Python Environment...${NC}"
pip install --break-system-packages --upgrade pip
pip install --break-system-packages requests[socks] colorama beautifulsoup4 lxml urllib3 maigret

# 4. MAIGRET AUTO-FIX (Permanent Solution)
echo -e "${G}[*] Setting up Maigret Global Path...${NC}"
# Maigret ko locate karke global bin mein link karna
MAIGRET_BIN=$(which maigret || find / -name maigret -type f 2>/dev/null | grep bin | head -n 1)

if [ -z "$MAIGRET_BIN" ]; then
    # Agar pip se path nahi mila toh manual link assume karein
    MAIGRET_BIN="/usr/local/bin/maigret"
fi

# Force link to ensure 'maigret' command works everywhere
ln -sf $(which maigret || echo "/usr/local/bin/maigret") /usr/bin/maigret

# 5. TOR SERVICE AUTO-START
echo -e "${G}[*] Starting Tor Service...${NC}"
systemctl enable tor
systemctl restart tor

# 6. SETUP PERMISSIONS
chmod +x khalid-osint.py
mkdir -p reports

echo -e "${C}----------------------------------------------------${NC}"
echo -e "${G}[SUCCESS] Sab kuch auto-install ho gaya hai!${NC}"
echo -e "${G}[➔] Ab aap direct run karein: python3 khalid-osint.py${NC}"
echo -e "${C}----------------------------------------------------${NC}"
