#!/bin/bash
# Khalid Husain - Telegram Bot Style OSINT Engine
echo -e "\e[1;32m[*] Installing Deep Crawlers & Leak Database Links...\e[0m"

# 1. Force release locks
sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# 2. Installing Core OSINT Engines
pip install colorama requests phonenumbers fpdf holehe maigret scylla-sh social-analyzer --break-system-packages --ignore-installed

# 3. Setting up Local Tool Directories
mkdir -p reports/targets tools/scylla tools/social-analyzer
cd tools
git clone --depth=1 https://github.com/SamueleAmato/SocialMediaHackingToolkit.git 2>/dev/null
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] OSINT BOT ENGINE READY! Run: python3 khalid-osint.py\e[0m"
