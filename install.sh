#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Fix: Bypass System Environment Errors (Superfast Mode)

echo -e "\e[1;32m[*] Installing Khalid OSINT Master Suite (No Errors)...\e[0m"

# Required Packages (No Upgrade to prevent lag)
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl wget

# Setup Virtual Environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Installing All Pro Tools & Modules
pip install --upgrade pip
pip install colorama requests phonenumbers holehe maigret haveibeenpwned photon-cli fpdf

# Reports Folder setup
mkdir -p reports

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] Setup Complete! Run: source venv/bin/activate && python3 khalid-osint.py\e[0m"
