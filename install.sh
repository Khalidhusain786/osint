#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Fix: Automated Fix for PIP Environment Errors

echo -e "\e[1;32m[*] Setup Start: Khalid OSINT Pro...\e[0m"

# Folder setup
mkdir -p reports

# System update (No upgrade to avoid lag)
sudo apt update 

# Install Essential Python Tools
sudo apt install -y python3-pip python3-venv git curl

# Installing Tools with --break-system-packages (Kali 2024+ Fix)
echo "[*] Installing Social & Phone Analyzers..."
pip3 install maigret holehe haveibeenpwned photon-cli colorama requests phonenumbers --break-system-packages --ignore-installed

# Sherlock Setup
if [ ! -d "$HOME/sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git $HOME/sherlock
    cd $HOME/sherlock && pip3 install -r requirements.txt --break-system-packages && cd -
fi

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] Perfect! Ab error nahi aayega. Run: python3 khalid-osint.py\e[0m"
