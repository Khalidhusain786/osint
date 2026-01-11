#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Feature: Auto-Lock Release & Self-Healing Setup

echo -e "\e[1;32m[*] Khalid OSINT: Fixing System Locks & Building Engine...\e[0m"

# 1. Force release apt locks (Screenshot 11 ka fix)
sudo rm /var/lib/dpkg/lock-frontend 2>/dev/null
sudo rm /var/lib/apt/lists/lock 2>/dev/null

# 2. Setup folders
mkdir -p reports/pdf reports/txt tools modules

# 3. Installing dependencies with "Error-Bypass" flag
sudo apt update
sudo apt install -y python3 python3-pip python3-full git curl wget
pip install --upgrade pip --break-system-packages

# 4. Installing professional libraries directly
pip install colorama requests phonenumbers fpdf flask pyfiglet holehe maigret --break-system-packages --ignore-installed

# 5. Local Tools (Direct Folder Access)
cd tools
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null
git clone --depth=1 https://github.com/soxoj/maigret.git 2>/dev/null
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] IMMORTAL SETUP READY! Run: python3 khalid-osint.py\e[0m"
