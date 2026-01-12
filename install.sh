#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports
echo -e "\e[34m[*] Installing OSINT Tools & HTML Cleaner...\e[0m"

# Installing required tools and HTML parser
python3 -m pip install --user colorama requests[socks] holehe sherlock-project maigret blackbird photon phoneinfoga beautifulsoup4

# Linking binaries
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/blackbird /usr/local/bin/blackbird
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga

echo -e "\e[32m[✔] Setup Ready!\e[0m"
