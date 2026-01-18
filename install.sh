#!/bin/bash

# --- CONFIGURATION ---
REPO_URL="https://github.com/Khalidhusain786/osint.git"
INSTALL_DIR="$HOME/osint"

# Colors for better visibility
GREEN='\033[0-32m'
RED='\033[0-31m'
NC='\033[0m' # No Color

echo -e "${GREEN}[+] OSINT Setup starting...${NC}"

# 1. Clean old directory if exists
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${GREEN}[+] Cleaning old osint directory...${NC}"
    rm -rf "$INSTALL_DIR"
fi

# 2. Clone Repository
echo -e "${GREEN}[+] Cloning repository...${NC}"
git clone "$REPO_URL" "$INSTALL_DIR" || { echo -e "${RED}Clone failed!${NC}"; exit 1; }

# 3. Enter Directory and Install
cd "$INSTALL_DIR" || exit
chmod +x install.sh

echo -e "${GREEN}[+] Running install.sh...${NC}"
sudo ./install.sh

# 4. Maigret Path Fix (The Smart Way)
echo -e "${GREEN}[+] Configuring Maigret symlink...${NC}"
MAIGRET_PATH=$(which maigret || echo "$HOME/.local/bin/maigret")

if [ -f "$MAIGRET_PATH" ]; then
    sudo ln -sf "$MAIGRET_PATH" /usr/bin/maigret
    echo -e "${GREEN}[+] Maigret linked successfully.${NC}"
else
    echo -e "${RED}[!] Warning: Maigret binary not found in common paths.${NC}"
fi

# 5. Services Restart
echo -e "${GREEN}[+] Restarting TOR service...${NC}"
sudo service tor restart

# 6. Final Clean and Run
clear
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   KHALID OSINT SETUP COMPLETED       ${NC}"
echo -e "${GREEN}========================================${NC}"

if [ -f "khalid-osint.py" ]; then
    python3 khalid-osint.py
else
    echo -e "${RED}[!] Error: khalid-osint.py not found in $INSTALL_DIR${NC}"
fi
