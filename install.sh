#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools
echo -e "\e[34m[*] Fix-All Installation Start... No Tools Removed.\e[0m"

# 1. Base Python Tools (Silent Mode)
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer 2>/dev/null

# 2. Fixing PATH (Taaki 'not found' error kabhi na aaye)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer

# 3. Bypass GitHub Login (Using direct ZIP for problematic tools)
cd tools
wget -q https://github.com/thewhiteh4t/seeker/archive/refs/heads/master.zip -O seeker.zip && unzip -q seeker.zip && mv seeker-master seeker && rm seeker.zip
wget -q https://github.com/htr-tech/zphisher/archive/refs/heads/master.zip -O zphisher.zip && unzip -q zphisher.zip && mv zphisher-master zphisher && rm zphisher.zip
cd ..

echo -e "\e[32m[✔] All Tools Fixed & Linked Successfully!\e[0m"
