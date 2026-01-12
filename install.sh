#!/bin/bash

# Rangon ka prayog (Formatting)
GREEN='\e[1;32m'
BLUE='\e[1;34m'
RED='\e[1;31m'
NC='\e[0m' # No Color

echo -e "${BLUE}[*] Khalid Shadow Bureau Setup Start Ho Raha Hai...${NC}"

# 1. System Update aur Basic Tools
echo -e "${BLUE}[*] Updating System Packages...${NC}"
sudo apt-get update -y && sudo apt-get install -y python3-pip tor torsocks curl lxml

# 2. Tor Service Setup
echo -e "${BLUE}[*] Tor Service Check Kar Rahe Hain...${NC}"
sudo systemctl enable tor
sudo systemctl start tor

# 3. Python Libraries (Specifically version fix ke sath taaki koi conflict na ho)
echo -e "${BLUE}[*] Python Libraries Install Kar Rahe Hain...${NC}"
# 'requests[socks]' onion routing ke liye zaroori hai
pip3 install --upgrade pip
pip3 install requests[socks] beautifulsoup4 colorama lxml urllib3 PySocks

# 4. Sherlock aur Maigret (OSINT Tools)
# Inhe pip se install karna sabse safe hai
echo -e "${BLUE}[*] OSINT Tools (Sherlock/Maigret) Setup...${NC}"
pip3 install sherlock maigret social-analyzer

# 5. Final Connection Test
echo -e "${BLUE}[*] Tor Connection Verify Kar Rahe Hain...${NC}"
TOR_CHECK=$(torsocks curl -s https://check.torproject.org | grep -i "Congratulations")

if [[ $TOR_CHECK == *"Congratulations"* ]]; then
    echo -e "${GREEN}[✔] Setup Successful! Tor Proxy Properly Kaam Kar Raha Hai.${NC}"
else
    echo -e "${RED}[!] Tor install toh ho gaya hai par connection slow ya block hai.${NC}"
    echo -e "${RED}[!] 'sudo service tor restart' try karein.${NC}"
fi

echo -e "${GREEN}Ab aap scan chala sakte hain: python3 khalid-osint.py${NC}"
