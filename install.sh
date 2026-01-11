#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Original No-Error Setup

echo -e "\e[1;32m[*] System Repairing & Tool Setup Starting...\e[0m"

# 1. Kill Locks & Fix Broken Packages
sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a
sudo apt-get install -f -y

# 2. Essential Folders
mkdir -p reports/targets tools

# 3. Installing Stable Modules (Bypassing Errors)
pip install colorama requests phonenumbers fpdf holehe maigret --break-system-packages --ignore-installed

# 4. Clone Professional Engines
cd tools
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null
git clone --depth=1 https://github.com/soxoj/maigret.git 2>/dev/null
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] SETUP DONE! Run: python3 khalid-osint.py\e[0m"
