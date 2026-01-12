#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports
echo -e "\e[34m[*] Cleaning old tools & installing HTML filters...\e[0m"

# Installing required cleaner
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret

# Linking tools to system path
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret

echo -e "\e[32m[✔] Clean Suite Ready!\e[0m"
