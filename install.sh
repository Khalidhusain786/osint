#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Fast Installer (No System Upgrade)

echo -e "\e[1;32m[*] Installing Dependencies for Khalid-OSINT-Pro...\e[0m"

# System update (no upgrade)
sudo apt update 

# Install core packages
sudo apt install -y python3 python3-pip git curl snapd

# Create required directories
mkdir -p reports

# Install OSINT tools via pip
echo "[*] Installing Holehe, Maigret, and Social Analyzers..."
pip3 install maigret holehe haveibeenpwned photon-cli colorama requests --break-system-packages

# Setup Sherlock (Username search)
if [ ! -d "~/sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git ~/sherlock
    cd ~/sherlock && pip3 install -r requirements.txt --break-system-packages && cd -
fi

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] Setup Complete by Khalid Husain! Run: python3 khalid-osint.py\e[0m"
