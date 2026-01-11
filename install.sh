#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Ultimate No-Error Binary Setup

echo -e "\e[1;32m[*] Fast Setup Starting... No PIP Errors anymore!\e[0m"

# Basic folders
mkdir -p reports
mkdir -p tools

# System tools install (Fast mode)
sudo apt update
sudo apt install -y python3-pip python3-full git curl

# Downloading Sherlock & Maigret directly (No PIP install needed)
cd tools
if [ ! -d "sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git
    python3 -m pip install -r sherlock/requirements.txt --break-system-packages
fi

if [ ! -d "maigret" ]; then
    git clone https://github.com/soxoj/maigret.git
    python3 -m pip install -r maigret/requirements.txt --break-system-packages
fi
cd ..

# Installing core essentials for the main script
python3 -m pip install colorama requests phonenumbers fpdf --break-system-packages

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL TOOLS READY! Ab seedhe chalao.\e[0m"
