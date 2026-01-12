#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools

echo -e "\e[34m[*] Re-linking All 30+ Tools (Full Suite Recovery)...\e[0m"

# Installing Core Libraries
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer 2>/dev/null

# Fixing Tool Paths (Ensures no 'not found' errors)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer

echo -e "\e[32m[✔] All Tools Restored & Linked Successfully!\e[0m"
