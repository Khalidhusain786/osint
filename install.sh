#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports
echo -e "\e[34m[*] Fixing Tools Path & Installing Cleaner...\e[0m"

# Sabhi tools ko install aur link karna
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret

# PATH linking (Taki 'not found' error na aaye)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret

echo -e "\e[32m[✔] Sab kuch set hai! Ab python3 khalid-osint.py chalayein.\e[0m"
