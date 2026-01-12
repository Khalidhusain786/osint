#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports
echo -e "\e[34m[*] Installing OSINT Suite & Auto-Submit Engine...\e[0m"

# dependencies install karna
python3 -m pip install --user colorama requests[socks] holehe sherlock-project maigret blackbird beautifulsoup4

# Sabhi tools ko path se link karna
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/blackbird /usr/local/bin/blackbird

echo -e "\e[32m[✔] Setup Ready! Saare tools link ho chuke hain.\e[0m"
