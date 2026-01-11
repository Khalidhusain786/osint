#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Fix: No system upgrade to prevent hanging

echo -e "\e[1;32m[*] Fast Installing Professional OSINT Tools (No Hang)...\e[0m"

# System Update (Sirf list update hogi, upgrade nahi)
sudo apt update 

# Zaruri dependencies (No Upgrade)
sudo apt install -y python3 python3-pip git curl snapd

# Reports folder ki mistake fix karne ke liye
mkdir -p reports

# Professional Tools (Fast Installation)
echo "[*] Installing Social & Breach Analyzers..."
pip3 install maigret holehe haveibeenpwned photon-cli colorama requests phonenumbers --break-system-packages

# Sherlock Setup (Fixed Path)
if [ ! -d "$HOME/sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git $HOME/sherlock
    cd $HOME/sherlock && pip3 install -r requirements.txt --break-system-packages && cd -
fi

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] Perfect Setup Done! Ab python3 khalid-osint.py chalao.\e[0m"
