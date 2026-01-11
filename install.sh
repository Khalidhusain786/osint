#!/bin/bash
# Khalid Husain Ultimate OSINT Suite Installer
# One-Click Setup - No Errors - No Upgrade Required

echo -e "\e[1;32m[*] Khalid OSINT Master Suite: Auto-Setup Starting...\e[0m"

# Required folders
mkdir -p reports/pdf reports/json reports/txt tools data/leaks

# Dependencies (Bypassing System PIP Errors)
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl wget

# Essential Libraries
python3 -m pip install colorama requests phonenumbers fpdf flask pyfiglet holehe maigret --break-system-packages --ignore-installed

# Auto-Download Professional Engines
cd tools
git clone --depth=1 https://github.com/sherlock-project/sherlock.git
git clone --depth=1 https://github.com/soxoj/maigret.git
git clone --depth=1 https://github.com/pypa/sampleproject.git # Placeholder for custom modules
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL TOOLS DOWNLOADED & READY. Run: python3 khalid-osint.py\e[0m"
