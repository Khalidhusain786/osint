#!/bin/bash
# Khalid Husain Immortal Engine - Emergency Fixer
# Force-clears all system locks and broken dependencies

echo -e "\e[1;32m[*] Khalid OSINT: Fixing System (Emergency Mode)...\e[0m"

# 1. Kill any process holding the lock (Screenshot 19:21 & 19:25 fix)
sudo fuser -kk /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock /var/cache/apt/archives/lock 2>/dev/null
sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock /var/cache/apt/archives/lock

# 2. Fix broken packages (Screenshot 19:31 fix)
sudo dpkg --configure -a
sudo apt-get install -f -y

# 3. Setup local environment
mkdir -p reports/txt tools modules

# 4. Install only core libraries (Fast & Safe)
# Using --break-system-packages to force bypass Kali's protection
pip install colorama requests phonenumbers fpdf holehe maigret --break-system-packages --ignore-installed

# 5. Clone tool dependencies locally
cd tools
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null || (cd sherlock && git pull)
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] SYSTEM FIXED! Ab 'python3 khalid-osint.py' chalaein.\e[0m"
