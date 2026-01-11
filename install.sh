#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Perfect No-Error Installer

echo -e "\e[1;32m[*] Installing Dependencies (Fast Mode)...\e[0m"

# Sirf update, no upgrade
sudo apt update 

# Zaruri tools install ho rahe hain
sudo apt install -y python3 python3-pip git curl snapd

# Directory setup
mkdir -p reports

# Pip tools installation
pip3 install maigret holehe haveibeenpwned photon-cli colorama requests phonenumbers --break-system-packages

# Sherlock Setup (Fixed Path)
if [ ! -d "$HOME/sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git $HOME/sherlock
    cd $HOME/sherlock && pip3 install -r requirements.txt --break-system-packages && cd -
fi

echo -e "\e[1;34m[!] Setup Complete Khalid! Run: python3 khalid-osint.py\e[0m"
