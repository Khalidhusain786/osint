#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Ultimate No-Error Fix for Kali 2024/2025

echo -e "\e[1;32m[*] Fast Setup Starting... No Hang, No Errors!\e[0m"

# Create reports folder first
mkdir -p reports

# Install critical system dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git curl snapd

# Fix for "ModuleNotFoundError" and PIP Environment
echo "[*] Installing core modules..."
pip3 install urllib3 requests colorama phonenumbers --break-system-packages --ignore-installed

# Force install OSINT tools
echo "[*] Installing OSINT Engines..."
pip3 install holehe maigret haveibeenpwned photon-cli --break-system-packages

# Sherlock Setup (Permanent Path)
if [ ! -d "$HOME/sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git $HOME/sherlock
    cd $HOME/sherlock && pip3 install -r requirements.txt --break-system-packages && cd -
fi

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] SETUP COMPLETE! Ab tool bina kisi error ke chalega.\e[0m"
