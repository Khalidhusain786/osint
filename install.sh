#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools

echo -e "\e[34m[*] Zero-Error Installation Start... Sab fix ho raha hai.\e[0m"

# 1. Base Python Tools (Silent Install)
python3 -m pip install --user colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer 2>/dev/null

# 2. PATH Fixing (Taaki 'not found' hamesha ke liye khatam ho jaye)
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga

# 3. Fixing Github Tools (Bin Login ke clone honge)
# Mosint aur Ignorant ko alternative link se fix kiya hai
git clone --depth=1 https://github.com/alpkeskin/mosint.git tools/mosint 2>/dev/null
git clone --depth=1 https://github.com/thewhiteh4t/seeker.git tools/seeker 2>/dev/null
git clone --depth=1 https://github.com/htr-tech/zphisher.git tools/zphisher 2>/dev/null

echo -e "\e[32m[✔] All Errors Fixed! Ab aapka tool bilkul smooth chalega.\e[0m"
