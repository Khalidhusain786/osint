#!/bin/bash
# Khalid Husain - Ultimate Framework Setup

echo -e "\e[1;32m[*] 6-Layer OSINT Framework Install ho raha hai...\e[0m"

# 1. Background Services
sudo apt update && sudo apt install tor whois dnsutils python3-pip -y
sudo service tor start

# 2. Advanced Engines
echo -e "\e[1;33m[*] Downloading Search Engines & Mirror Scrapers...\e[0m"
pip install colorama requests[socks] holehe maigret social-analyzer --break-system-packages --ignore-installed

# 3. Path & Permissions
mkdir -p /root/osint/reports
chmod +x khalid-osint.py

echo -e "\e[1;34m[!] Framework Taiyar! Ab 'python3 khalid-osint.py' chalaein.\e[0m"
