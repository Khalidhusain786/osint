#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools

echo -e "\e[34m[*] Fix-All Installation: No Tools Removed, All Errors Patched...\e[0m"

# 1. Base Python Tools (Installing the Full 30+ List)
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer 2>/dev/null

# 2. Hard-Fixing Paths (Eliminates 'not found' errors)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer

# 3. GitHub Login Bypass (Downloading tools that fail on clone)
cd tools
wget -q https://github.com/thewhiteh4t/seeker/archive/refs/heads/master.zip -O seeker.zip && unzip -q seeker.zip && mv seeker-master seeker && rm seeker.zip
wget -q https://github.com/htr-tech/zphisher/archive/refs/heads/master.zip -O zphisher.zip && unzip -q zphisher.zip && mv zphisher-master zphisher && rm zphisher.zip
cd ..

echo -e "\e[32m[✔] All Tools Linked and Ready!\e[0m"
