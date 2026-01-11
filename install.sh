#!/bin/bash
# Khalid Husain - Global Deep/Dark Web Integration
echo -e "\e[1;32m[*] Installing 6-Layer Global Infrastructure...\e[0m"

# System Clean & TOR Setup
sudo apt update && sudo apt install tor proxychains4 macchanger -y
sudo service tor start

# Core Python Tools (Stable Versions)
pip install colorama requests[socks] yagmail fpdf holehe maigret social-analyzer --break-system-packages --ignore-installed

# Creating Database Folders
mkdir -p reports/targets reports/darkweb_leaks

echo -e "\e[1;34m[!] ALL TOOLS LOADED. Run: python3 khalid-osint.py\e[0m"
