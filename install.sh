#!/bin/bash
# Khalid Husain Immortal Engine v25
# Force-Fix System & Tool Integration

echo -e "\e[1;32m[*] System Repairing & Tool Setup Starting...\e[0m"

# 1. Fix Broken Packages & Locks (Screenshot 19:31 fix)
sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a
sudo apt-get install -f -y

# 2. Setup Folders for Automated Saving
mkdir -p reports/targets tools

# 3. Direct Library Injection (Bypassing wheel errors)
pip install colorama requests phonenumbers fpdf holehe maigret --break-system-packages --ignore-installed --no-cache-dir

# 4. Clone Professional Engines Locally
cd tools
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null
git clone --depth=1 https://github.com/soxoj/maigret.git 2>/dev/null
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL TOOLS INTEGRATED! Run: python3 khalid-osint.py\e[0m"
