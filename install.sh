#!/bin/bash

# System update aur Tor setup
echo -e "\e[34m[*] Updating system and installing Tor...\e[0m"
sudo apt-get update -y
sudo apt-get install -y tor torsocks python3-pip libxml2-dev libxslt1-dev zlib1g-dev

# Python libraries (No-error mode for Kali Linux)
echo -e "\e[32m[*] Installing Python dependencies (BS4, LXML, Colorama)...\e[0m"
pip3 install --upgrade pip --break-system-packages
pip3 install requests beautifulsoup4 lxml colorama --break-system-packages

# Tor service ko background mein on karna
echo -e "\e[34m[*] Restarting Tor Service...\e[0m"
sudo systemctl enable tor
sudo service tor restart

echo -e "\e[36m[✔] Setup Complete! Naya Accurate Code chalane ke liye taiyar hai.\e[0m"
