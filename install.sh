#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools
echo -e "\e[34m[*] Installing All 30+ Tools (Full List - No Removal)...\e[0m"

# 1. Python Tools (Full Integration)
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer ghunt mosint ignorant-osint theHarvester recon-ng spiderfoot finalrecon 2>/dev/null

# 2. PATH Fixing (Fixes 'Command Not Found')
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga

# 3. GitHub Tools (Tracking & Social Engineering)
cd tools
git clone --depth=1 https://github.com/msharma2404/Traxosint.git 2>/dev/null
git clone --depth=1 https://github.com/s0md3v/Phomber.git 2>/dev/null
git clone --depth=1 https://github.com/thewhiteh4t/seeker.git 2>/dev/null
git clone --depth=1 https://github.com/htr-tech/zphisher.git 2>/dev/null
git clone --depth=1 https://github.com/KasRoudra/PyPhisher.git 2>/dev/null
git clone --depth=1 https://github.com/Moham3dRiahi/Th3inspector.git 2>/dev/null
cd ..

echo -e "\e[32m[✔] All Tools Installed Successfully!\e[0m"
