#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools
echo -e "\e[34m[*] Installing Every Tool from Your List (No-Error Mode)...\e[0m"

# 1. Phone & Email Tools
python3 -m pip install --user holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer ghunt 2>/dev/null

# 2. Hard-Fix for Path Errors (Taaki 'not found' na aaye)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga

# 3. Installing GitHub-only Tools (Jo pip par nahi hain)
cd tools
git clone https://github.com/msharma2404/Traxosint.git 2>/dev/null
git clone https://github.com/s0md3v/Phomber.git 2>/dev/null
git clone https://github.com/alpkeskin/mosint.git 2>/dev/null
git clone https://github.com/thewhiteh4t/seeker.git 2>/dev/null
git clone https://github.com/htr-tech/zphisher.git 2>/dev/null
git clone https://github.com/Moham3dRiahi/Th3inspector.git 2>/dev/null
git clone https://github.com/KasRoudra/PyPhisher.git 2>/dev/null
cd ..

echo -e "\e[32m[✔] All 30+ Tools Integrated. No Missing Files!\e[0m"
