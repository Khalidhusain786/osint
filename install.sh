#!/bin/bash

# Purana kachra saaf karne ke liye
echo -e "\e[31m[*] Cleaning old files...\e[0m"
rm -rf /home/kali/osint

# System update aur Tor setup
echo -e "\e[34m[*] Updating system and installing Tor...\e[0m"
sudo apt-get update -y
sudo apt-get install -y tor torsocks python3-pip libxml2-dev libxslt1-dev zlib1g-dev

# Python libraries jo naye code ke liye zaroori hain
echo -e "\e[32m[*] Installing Python dependencies (BS4, LXML, Colorama)...\e[0m"
pip3 install --upgrade pip
pip3 install requests beautifulsoup4 lxml colorama

# Tor service ko auto-start karna
sudo service tor restart

echo -e "\e[36m[✔] Setup Complete! No errors expected.\e[0m"
