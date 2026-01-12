#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports
echo -e "\e[34m[*] Configuring Final OSINT Suite...\e[0m"

# Dependencies
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret

# Linking binaries for immediate use
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret

echo -e "\e[32m[✔] Setup Ready! Run: python3 khalid-osint.py\e[0m"
