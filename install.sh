#!/bin/bash
echo -e "\e[1;32m[*] Khalid-OSINT: Installing Your Tool List...\e[0m"

# 1. System Essentials
sudo apt update && sudo apt install python3-pip curl git nodejs npm googler tor proxychains4 -y

# 2. Main OSINT Engines (Fixing Dependencies)
pip install colorama requests[socks] telethon holehe maigret sherlock socialscan ghunt instaloader --break-system-packages

# 3. Cloning Repository Tools (Seeker, Zphisher, etc.)
mkdir -p tools
cd tools
git clone https://github.com/thewhiteh4t/seeker.git
git clone https://github.com/htr-tech/zphisher.git
git clone https://github.com/sundowndev/phoneinfoga.git
git clone https://github.com/Lucksi/Mr-Holmes.git
cd ..

mkdir -p reports
echo -e "\e[1;34m[✔] All Tools Ready in /home/kali/osint/tools/\e[0m"
