#!/bin/bash
# Khalid Husain Immortal OSINT - Setup v40
echo -e "\e[1;32m[*] Telegram Bot Style Engine Setup Starting...\e[0m"

# Force release locks
sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# Folders for unlimited data storage
mkdir -p reports/targets tools modules

# Installing Deep-Scan Libraries
pip install colorama requests phonenumbers fpdf holehe maigret scylla-sh social-analyzer --break-system-packages --ignore-installed

# Cloning Master Tools
cd tools
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null
git clone --depth=1 https://github.com/soxoj/maigret.git 2>/dev/null
git clone --depth=1 https://github.com/SamueleAmato/SocialMediaHackingToolkit.git 2>/dev/null
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] NO-LIMIT ENGINE READY! Run: python3 khalid-osint.py\e[0m"
