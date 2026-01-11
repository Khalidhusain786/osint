#!/bin/bash
# Khalid Husain - Ultimate Bot Engine Setup
echo -e "\e[1;32m[*] Installing Scylla and Telegram Bot Modules...\e[0m"

# 1. System Fix
sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# 2. Scylla Installation (Correct Source)
mkdir -p tools
cd tools
git clone https://github.com/cybersecurity-team/Scylla.git
cd Scylla
pip install -r requirements.txt --break-system-packages
cd ../..

# 3. Social & Phone Modules
pip install colorama requests phonenumbers holehe maigret social-analyzer --break-system-packages --ignore-installed

# 4. Permissions
chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL BOTS INTEGRATED! Run: python3 khalid-osint.py\e[0m"
