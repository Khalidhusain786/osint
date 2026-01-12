#!/bin/bash
echo -e "\e[1;32m[*] System Fix aur Deep Installation Shuru...\e[0m"

# 1. Broken Packages Fix
sudo apt update --fix-missing
sudo apt install -y python3-pip curl git nodejs npm googler tor proxychains4 libpcap-dev

# 2. Python Tools Fix (Direct Installation)
# System environment bypass karke install karna
python3 -m pip install --upgrade pip --break-system-packages
python3 -m pip install colorama requests[socks] telethon holehe maigret sherlock social-analyzer ghunt --break-system-packages

# 3. Dedicated Tools (Sirf wahi jo login nahi maangte)
mkdir -p tools && cd tools
rm -rf seeker zphisher phoneinfoga # Purana saaf karna
git clone https://github.com/thewhiteh4t/seeker.git
git clone https://github.com/htr-tech/zphisher.git
git clone https://github.com/sundowndev/phoneinfoga.git
cd ..

mkdir -p reports
echo -e "\e[1;34m[✔] Setup Ready! Saare errors fix kar diye gaye hain.\e[0m"
