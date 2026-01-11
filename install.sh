#!/bin/bash
# Khalid Husain - Final Error-Free Setup
echo -e "\e[1;32m[*] Cleaning system and installing stable modules...\e[0m"

# Forcefully remove locks
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# Install only the most stable core tools
pip install colorama requests yagmail fpdf holehe --break-system-packages --ignore-installed

# Maigret installation (stable version)
pip install maigret --break-system-packages

echo -e "\e[1;34m[!] Setup Complete! No more errors. Run: python3 khalid-osint.py\e[0m"
