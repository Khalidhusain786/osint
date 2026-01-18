#!/bin/bash

# --- CONFIGURATION ---
REPO_URL="https://github.com/Khalidhusain786/osint.git"
INSTALL_DIR="/home/kali/osint"

# Colors for status
GREEN='\033[0-32m'
BLUE='\033[0-34m'
RED='\033[0-31m'
NC='\033[0m'

echo -e "${BLUE}[*] Full Automation Started...${NC}"

# 1. Update and Install Auto-Fixer Tool
echo -e "${GREEN}[+] Installing Python auto-formatter (autopep8)...${NC}"
sudo apt update -y && sudo apt install -y python3-pip
pip3 install autopep8 --break-system-packages 2>/dev/null

# 2. Cleanup and Clone
echo -e "${GREEN}[+] Cleaning and Cloning Repository...${NC}"
sudo rm -rf "$INSTALL_DIR"
cd /home/kali
git clone "$REPO_URL" "$INSTALL_DIR"
cd "$INSTALL_DIR" || exit

# 3. Permissions and Installation
echo -e "${GREEN}[+] Running Installation Script...${NC}"
chmod +x install.sh
sudo ./install.sh

# 4. AUTO-FIX PYTHON ERRORS (Indentation Fix)
echo -e "${GREEN}[+] Automatically fixing Python Indentation Errors...${NC}"
if [ -f "khalid-osint.py" ]; then
    # Sabse pehle tabs ko spaces mein convert karega
    sed -i 's/\t/    /g' khalid-osint.py
    # Phir autopep8 poori coding style aur spacing theek kar dega
    python3 -m autopep8 --in-place --aggressive --aggressive khalid-osint.py
    echo -e "${GREEN}[✔] Python file fixed!${NC}"
else
    echo -e "${RED}[!] khalid-osint.py not found!${NC}"
fi

# 5. Maigret Symlink Fix
echo -e "${GREEN}[+] Setting up Maigret path...${NC}"
MA_PATH=$(which maigret || echo "$HOME/.local/bin/maigret")
sudo ln -sf "$MA_PATH" /usr/bin/maigret

# 6. Service Refresh
echo -e "${GREEN}[+] Restarting TOR...${NC}"
sudo service tor restart

# 7. Final Step: Run
clear
echo -e "${GREEN}======================================"
echo -e "   SETUP DONE - STARTING KHALID OSINT"
echo -e
