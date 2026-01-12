#!/bin/bash
echo -e "\e[1;32m[*] Auto-Fixer Installation Shuru...\e[0m"

# 1. System Fix (Missing Googler fix)
sudo apt update
sudo apt install -y python3-pip curl git tor proxychains4 libpcap-dev
sudo curl -o /usr/local/bin/googler https://raw.githubusercontent.com/jarun/googler/master/googler
sudo chmod +x /usr/local/bin/googler

# 2. Pip Fix (Environment Bypass)
python3 -m pip install --user --break-system-packages colorama requests[socks] telethon holehe maigret sherlock

# 3. Path Fix (Taaki 'Not Found' error na aaye)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe

echo -e "\e[1;34m[✔] Sab Fix Ho Gaya! Ab script chalao.\e[0m"
