#!/bin/bash
# KHALID-OSINT MASTER INSTALLER v39.0 (ZERO DELETION)

echo -e "\e[32m[+] Starting Khalid-OSINT Fixed Installation...\e[0m"

# 1. System Update & Missing Repos Fix (Screenshot error solve)
sudo apt-get update --fix-missing
sudo apt install -y tor libimage-exiftool-perl wkhtmltopdf python3-pip git colorama

# 2. Pip Conflicts Fix (theHarvester/BS4 errors solve)
# Ek bhi line delete nahi, sirf naye versions ko fix kiya hai
python3 -m pip install --user --break-system-packages --ignore-installed \
requests[socks] colorama beautifulsoup4==4.13.4 lxml==6.0.0 jinja2 pdfkit \
holehe maigret sherlock h8mail truecallerpy aiohttp aiofiles

# 3. Tool Directories Restore (Fatal destination errors solve)
if [ ! -d "tools" ]; then mkdir tools; fi
[ -d "tools/Photon" ] || git clone https://github.com/s0md3v/Photon.git tools/Photon
[ -d "tools/blackbird" ] || git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird

# 4. Service Setup
sudo service tor start
chmod +x khalid-osint.py

echo -e "\e[32m[+] Sab kuch fix ho gaya hai! Ab aap ./install.sh ya python3 run kar sakte hain.\e[0m"
