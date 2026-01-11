#!/bin/bash
# Khalid Husain - Final Master Bot Setup
echo -e "\e[1;32m[*] Killing System Locks & Installing Unlimited Bot Modules...\e[0m"

# 1. Force Release Locks (Screenshot 19:21 & 19:25 fix)
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock /var/cache/apt/archives/lock

# 2. Fix Broken Dependencies (libc6 masla hal)
sudo dpkg --configure -a
sudo apt-get install -f -y

# 3. Install Core Libraries (No-Limit OSINT)
pip install colorama requests phonenumbers holehe maigret social-analyzer --break-system-packages --ignore-installed

# 4. Manual Scylla Setup (Bypassing requirements.txt missing error)
mkdir -p tools
cd tools
rm -rf Scylla 2>/dev/null
git clone --depth=1 https://github.com/cybersecurity-team/Scylla.git 2>/dev/null
# Scylla ki dependencies manually install karna
pip install requests beautifulsoup4 lxml --break-system-packages
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL TOOLS INTEGRATED! Run: python3 khalid-osint.py\e[0m"
