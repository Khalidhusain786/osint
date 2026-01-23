#!/bin/bash

# --- Colors for Output ---
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}[*] Starting OSINT Environment Setup...${NC}"

# 1. Update System Repositories
echo -e "${GREEN}[*] Updating system packages...${NC}"
sudo apt-get update -y

# 2. Install Core Dependencies
echo -e "${GREEN}[*] Installing Tor, Python3, and Pip...${NC}"
sudo apt-get install -y tor python3 python3-pip python3-venv socksjs-client

# 3. Configure and Start Tor Service
echo -e "${GREEN}[*] Configuring Tor service...${NC}"
sudo systemctl enable tor
sudo systemctl restart tor

# 4. Install Python Libraries
echo -e "${GREEN}[*] Installing Python requirements...${NC}"
pip3 install requests[socks] colorama beautifulsoup4 urllib3 --break-system-packages

# 5. Directory Cleanup & Permissions
echo -e "${GREEN}[*] Setting up report directories...${NC}"
mkdir -p reports
chmod +x *.py

echo -e "${GREEN}[✓] Setup Complete. Ensure Tor is running (127.0.0.1:9050)${NC}"
