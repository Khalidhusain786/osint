#!/bin/bash

# --- CONFIG ---
TARGET="7696408248"
INSTALL_DIR="/home/kali/osint"

echo -e "\e[1;34m[*] Starting Khalid OSINT Automation...\e[0m"

# 1. Environment Cleanup & Repo Clone
cd /home/kali
sudo rm -rf osint
git clone https://github.com/Khalidhusain786/osint.git
cd osint || { echo "Failed to enter directory"; exit 1; }

# 2. Permissions & Installation
chmod +x install.sh
sudo ./install.sh

# 3. Dependencies Fix (Breaking System Packages Fix for Kali)
echo -e "\e[1;32m[+] Installing required Python modules...\e[0m"
pip3 install playwright stem aiohttp --break-system-packages 2>/dev/null
python3 -m playwright install chromium --with-deps 2>/dev/null

# 4. Maigret Symlink Fix
echo -e "\e[1;32m[+] Setting up Maigret path...\e[0m"
sudo ln -sf $(which maigret || echo "$HOME/.local/bin/maigret") /usr/bin/maigret

# 5. Tor Service Configuration
echo -e "\e[1;32m[+] Restarting Tor Service...\e[0m"
sudo service tor restart
sleep 2

# 6. AUTO-FIX: Indentation Error in khalid-osint.py
# Yeh command line 3 ke indentation ko theek karega
echo -e "\e[1;32m[+] Fixing Python Indentation...\e[0m"
sed -i 's/^[ \t]*self.drops.extend/        self.drops.extend/' khalid-osint.py

# 7. Final Execution
clear
echo -e "\e[1;32m[!] Launching Khalid OSINT for target: $TARGET\e[0m"
python3 khalid-osint.py $TARGET
