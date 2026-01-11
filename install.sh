#!/bin/bash
# Khalid Husain - Global Deep-Scan Setup (Root Version)

echo -e "\e[1;32m[*] System cleanup aur installation shuru ho rahi hai...\e[0m"

# 1. System Cleanup
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# 2. Install Tools (TOR for Hidden Web)
sudo apt update
sudo apt install tor proxychains4 python3-pip -y
sudo service tor start

# 3. Install Searching Engines (No-Error Version)
pip install colorama requests[socks] holehe maigret social-analyzer --break-system-packages --ignore-installed

# 4. Folder structure setup
mkdir -p /root/osint/reports

echo -e "\e[1;34m[!] Setup Ready! Ab 'python3 khalid-osint.py' chala sakte hain.\e[0m"
