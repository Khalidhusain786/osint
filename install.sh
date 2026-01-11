#!/bin/bash
# Khalid Husain - Global Deep-Scan Setup (Root Version)

echo -e "\e[1;32m[*] System cleanup aur installation shuru ho rahi hai...\e[0m"

# 1. Purane locks aur kachra saaf karein
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# 2. Zaroori system packages (TOR aur Python Tools)
sudo apt update
sudo apt install tor proxychains4 python3-pip -y
sudo service tor start

# 3. Stable Python Modules (Maigret aur Holehe jo screenshots mein chahiye)
# Isme error-prone modules (googletrans) hata diye gaye hain
pip install colorama requests[socks] holehe maigret social-analyzer --break-system-packages --ignore-installed

# 4. Folder structure aur permission set karein
mkdir -p /root/osint/reports
chmod +x /root/osint/khalid-osint.py 2>/dev/null

echo -e "\e[1;34m[!] Setup Ready! Ab aap 'python3 khalid-osint.py' chala sakte hain.\e[0m"
