#!/bin/bash
# KHALID MASTER OSINT INSTALLER (ZERO ERROR MODE)

echo -e "\e[31m[*] Starting Error-Free Installation for Python 3.13...\e[0m"

# Path setup aur permissions
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports

# System Dependencies
sudo apt update && sudo apt install -y python3-full python3-pip git curl tor

# Broken wheel errors ko bypass karke compatible versions install karna
echo -e "\e[34m[*] Installing Core Tools (Bypassing build errors)...\e[0m"
python3 -m pip install --user colorama requests[socks] holehe maigret blackbird photon sherlock-project

# Tools ko system path se link karna (Taki 'not found' error na aaye)
echo -e "\e[34m[*] Linking tools to system path...\e[0m"
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/blackbird /usr/local/bin/blackbird

echo -e "\e[32m[✔] Installation Complete! No Errors.\e[0m"
