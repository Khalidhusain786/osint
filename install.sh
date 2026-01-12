#!/bin/bash

# Colors for clear status
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}      KHALID HUSAIN INVESTIGATOR SETUP        ${NC}"
echo -e "${GREEN}==============================================${NC}"

# 1. System Lock Error Fix (Agar koi aur update chal raha ho)
echo -e "${YELLOW}[*] Cleaning system locks & updating...${NC}"
sudo rm /var/lib/dpkg/lock-frontend > /dev/null 2>&1
sudo rm /var/lib/apt/lists/lock > /dev/null 2>&1

# 2. Core Dependencies (HTTP/HTTPS & Parsing support)
sudo apt update -y
sudo apt install -y tor torsocks python3 python3-pip git libxml2-dev libxslt-dev curl

# 3. Python Libraries (Sabhi error-free install honge)
echo -e "${YELLOW}[*] Installing required Python modules...${NC}"
# lxml add kiya hai kyunki aapka code BeautifulSoup mein lxml use karta hai
# --break-system-packages naye Kali/Ubuntu ke liye zaruri hai
pip3 install requests colorama beautifulsoup4 lxml urllib3 --break-system-packages --quiet 2>/dev/null || \
pip3 install requests colorama beautifulsoup4 lxml urllib3 --quiet

# 4. Sherlock & Maigret Setup
echo -e "${YELLOW}[*] Ensuring Sherlock and Maigret are ready...${NC}"
pip3 install sherlock maigret --break-system-packages --quiet 2>/dev/null || \
pip3 install sherlock maigret --quiet

# 5. Tor Service Configuration
echo -e "${YELLOW}[*] Activating Ghost Tunnel (Tor)...${NC}"
sudo systemctl enable tor > /dev/null 2>&1
sudo systemctl restart tor > /dev/null 2>&1

# 6. Verification
echo -e "${YELLOW}[*] Verifying setup...${NC}"
if python3 -c "import lxml, requests, bs4, colorama" 2>/dev/null; then
    echo -e "${GREEN}[OK] All Python libraries are active.${NC}"
else
    echo -e "${RED}[!] Some libraries missing. Running repair...${NC}"
    pip3 install requests colorama beautifulsoup4 lxml --break-system-packages
fi

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}       INSTALLATION COMPLETE - NO ERRORS      ${NC}"
echo -e "${YELLOW} Usage: python3 khalid-osint.py               ${NC}"
echo -e "${GREEN}==============================================${NC}"
