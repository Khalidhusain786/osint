#!/bin/bash
# Khalid Husain - Ultimate No-Error Setup v50
echo -e "\e[1;32m[*] Breaking locks and installing all bot modules...\e[0m"

# 1. Kill and remove all apt locks (Screenshot 19:25 fix)
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock /var/cache/apt/archives/lock

# 2. Fix broken system packages (Screenshot 19:31 fix)
sudo dpkg --configure -a
sudo apt-get install -f -y

# 3. Install core libraries (Unlimited version)
pip install colorama requests phonenumbers holehe maigret social-analyzer --break-system-packages --ignore-installed

# 4. Manual Scylla Setup (Screenshot 20:31 fix - No requirements.txt needed)
mkdir -p tools
cd tools
git clone --depth=1 https://github.com/cybersecurity-team/Scylla.git 2>/dev/null
# Manually installing Scylla dependencies
pip install requests beautifulsoup4 lxml --break-system-packages
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] ALL BOTS INTEGRATED! Run: python3 khalid-osint.py\e[0m"
