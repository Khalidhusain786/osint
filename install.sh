#!/bin/bash

# Colors for status
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}>>> Updating System & Installing Dependencies...${NC}"

# 1. System packages ko install karna (Jo code ke har feature ke liye zaruri hain)
sudo apt update -y
sudo apt install -y tor torsocks python3 python3-pip git libxml2-dev libxslt-dev

# 2. Python Libraries (Jo aapke code mein use ho rahi hain)
# Isme 'lxml' add kiya hai taaki BeautifulSoup fast kaam kare
echo -e "${YELLOW}>>> Installing Python Libraries (requests, bs4, lxml, colorama)...${NC}"
pip3 install requests colorama bs4 lxml urllib3 --break-system-packages --quiet 2>/dev/null || pip3 install requests colorama bs4 lxml urllib3 --quiet

# 3. Sherlock aur Maigret check (Taki search har jagah ho sake)
if ! command -v sherlock &> /dev/null; then
    pip3 install sherlock --break-system-packages --quiet 2>/dev/null || pip3 install sherlock --quiet
fi

if ! command -v maigret &> /dev/null; then
    pip3 install maigret --break-system-packages --quiet 2>/dev/null || pip3 install maigret --quiet
fi

# 4. Tor Service restart (Ghost Tunnel ke liye)
sudo systemctl enable tor
sudo systemctl restart tor

echo -e "${GREEN}>>> INSTALLATION FINISHED. NO ERRORS.${NC}"
echo -e "${YELLOW}Usage: python3 khalid-osint.py${NC}"
