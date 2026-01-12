#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools

echo -e "\e[34m[*] Fixing All Installation Errors & Linking Tools...\e[0m"

# Python Core Tools Installation (Mosint error fix kiya hai)
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer ghunt ignorant-osint

# Hard-Linking (Isse 'not found' error kabhi nahi aayega)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga

# Cloning Tools for tracking/phishing
git clone https://github.com/thewhiteh4t/seeker.git tools/seeker 2>/dev/null
git clone https://github.com/htr-tech/zphisher.git tools/zphisher 2>/dev/null
git clone https://github.com/Moham3dRiahi/Th3inspector.git tools/Th3inspector 2>/dev/null

echo -e "\e[32m[✔] All Errors Fixed! Social Analyzer is Linked.\e[0m"
