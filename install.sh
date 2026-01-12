#!/bin/bash
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports
echo -e "\e[34m[*] Installing Tools & Linking Paths...\e[0m"
python3 -m pip install --user colorama requests[socks] holehe sherlock-project maigret blackbird photon phoneinfoga
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret
sudo ln -sf ~/.local/bin/blackbird /usr/local/bin/blackbird
sudo ln -sf ~/.local/bin/phoneinfoga /usr/local/bin/phoneinfoga
echo -e "\e[32m[✔] All Tools Linked!\e[0m"
