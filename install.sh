#!/bin/bash

# Environment settings
export PIP_BREAK_SYSTEM_PACKAGES=1
mkdir -p reports tools

echo -e "\e[34m[*] Zero-Deletion Update: Recovering 30+ Tools...\e[0m"

# 1. Check if Python & Pip are installed
if ! command -v pip3 &> /dev/null; then
    echo -e "\e[31m[!] Pip3 not found. Installing...\e[0m"
    sudo apt update && sudo apt install -y python3-pip
fi

# 2. Python Core Update (Removed 2>/dev/null to see progress)
echo -e "\e[33m[*] Installing Python packages...\e[0m"
python3 -m pip install --user --upgrade colorama requests beautifulsoup4 holehe sherlock-project maigret blackbird photon phoneinfoga social-analyzer

# 3. List of tools to link
TOOLS=("sherlock" "holehe" "maigret" "phoneinfoga" "social-analyzer")

# 4. Automating the linking process
echo -e "\e[33m[*] Creating Symlinks...\e[0m"
for tool in "${TOOLS[@]}"; do
    if [ -f ~/.local/bin/$tool ]; then
        sudo ln -sf ~/.local/bin/$tool /usr/local/bin/$tool
        echo -e "\e[32m[✔] Linked: $tool\e[0m"
    else
        echo -e "\e[31m[!] Warning: $tool not found in ~/.local/bin\e[0m"
    fi
done

echo -e "\e[32m\n[✔] Setup Complete! No deletions made.\e[0m"
