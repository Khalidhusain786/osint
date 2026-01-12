#!/bin/bash
# KHALID MASTER INSTALLER
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports

echo -e "\e[34m[*] Installing Tools & Fixing Python 3.13 Errors...\e[0m"
# Incompatible build errors ko bypass karne ke liye tools install karna
python3 -m pip install --user colorama requests[socks] holehe sherlock-project maigret blackbird photon

# Sabhi tools ko system path se link karna
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/blackbird /usr/local/bin/blackbird

echo -e "\e[32m[✔] Setup Complete. Now run: python3 khalid-osint.py\e[0m"
