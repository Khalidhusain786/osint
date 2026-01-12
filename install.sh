#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools
echo -e "\e[34m[*] Installing All Tools (Priority: Anish Portal)...\e[0m"

# Python Tools Install
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer 2>/dev/null

# Fix Path Errors
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer

# Fix GitHub Login Error (Downloading directly)
cd tools
wget -q https://github.com/thewhiteh4t/seeker/archive/refs/heads/master.zip -O seeker.zip && unzip -q seeker.zip && mv seeker-master seeker && rm seeker.zip
wget -q https://github.com/htr-tech/zphisher/archive/refs/heads/master.zip -O zphisher.zip && unzip -q zphisher.zip && mv zphisher-master zphisher && rm zphisher.zip
cd ..

echo -e "\e[32m[✔] Setup Complete. Anish Portal is Priority #1.\e[0m"
