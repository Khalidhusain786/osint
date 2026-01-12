#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports
echo -e "\e[34m[*] Installing Full OSINT Suite (Phone, Email, Username, Web)...\e[0m"

# Installing tools from your list
python3 -m pip install --user colorama requests[socks] holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer ghunt

# Linking all tools to system path
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/blackbird /usr/local/bin/blackbird
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga
sudo ln -sf ~/.local/bin/photon /usr/local/bin/photon

echo -e "\e[32m[✔] All Tools Linked Successfully!\e[0m"
