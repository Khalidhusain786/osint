#!/bin/bash
# Khalid Husain - Dark Web TOR Integration Setup
echo -e "\e[1;32m[*] Installing TOR Connectors & Dark Web Scrapers...\e[0m"

# 1. System Repair & TOR Installation
sudo apt update && sudo apt install tor proxychains4 -y
sudo service tor start

# 2. Python TOR & Translation Libraries
pip install colorama requests[socks] yagmail fpdf holehe maigret \
            googletrans==4.0.0-rc1 --break-system-packages --ignore-installed

# 3. Directory for Dark Evidence
mkdir -p reports/targets reports/darkweb_leaks

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] TOR BRIDGE READY! Run: python3 khalid-osint.py\e[0m"
