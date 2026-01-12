#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools
echo -e "\e[34m[*] Installing Social Analyzer & 30+ OSINT Tools...\e[0m"

# Core Tools Installation
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer ghunt mosint ignorant-osint

# Linking Binaries (Fixes 'Not Found' error)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga

# Phishing & Tracking Tools
git clone https://github.com/thewhiteh4t/seeker.git tools/seeker 2>/dev/null
git clone https://github.com/htr-tech/zphisher.git tools/zphisher 2>/dev/null
git clone https://github.com/Moham3dRiahi/Th3inspector.git tools/Th3inspector 2>/dev/null

echo -e "\e[32m[✔] Social Analyzer and All Tools Ready!\e[0m"
