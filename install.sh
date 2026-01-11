#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Auto-Installer & System Fixer

echo -e "\e[1;32m[*] Khalid OSINT: Fixing Environment & Installing Tools...\e[0m"

# Folder creation
mkdir -p reports

# System Dependencies
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl

# Virtual Environment Setup (Error Bypass)
python3 -m venv venv
source venv/bin/activate

# Force Install all tools
pip install --upgrade pip
pip install colorama requests phonenumbers holehe maigret haveibeenpwned photon-cli fpdf --break-system-packages --ignore-installed

# Sherlock setup
if [ ! -d "$HOME/sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git $HOME/sherlock
    cd $HOME/sherlock && pip install -r requirements.txt && cd -
fi

echo -e "\e[1;34m[!] Setup Done! Ab bas 'python3 khalid-osint.py' chalao, activation auto hogi.\e[0m"
