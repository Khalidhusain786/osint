#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Ultimate No-Lag No-Error Installer

echo -e "\e[1;32m[*] Fast Setup Starting... Sab errors fix ho jayenge!\e[0m"

# Folder setup
mkdir -p reports

# Zaruri system files (Bina upgrade ke)
sudo apt update
sudo apt install -y python3-pip python3-venv git curl

# Sabse zaruri step: Virtual Environment banana taaki koi error na aaye
python3 -m venv venv
source venv/bin/activate

# Environment ke andar tools install karna
echo "[*] Installing Khalid's OSINT Engine..."
pip install --upgrade pip
pip install colorama requests phonenumbers holehe maigret haveibeenpwned photon-cli

# Sherlock Setup
if [ ! -d "$HOME/sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git $HOME/sherlock
    cd $HOME/sherlock && pip install -r requirements.txt && cd -
fi

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] SETUP DONE! Ab bas ye command chalao: source venv/bin/activate && python3 khalid-osint.py\e[0m"
