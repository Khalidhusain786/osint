#!/bin/bash

echo "[*] Installing Dependencies..."

# System Updates
sudo apt-get update
sudo apt-get install -y tor torsocks python3 python3-pip lxml

# Python Libraries
pip install requests beautifulsoup4 colorama lxml

# Tools (If not installed)
# pip install sherlock maigret social-analyzer

echo "[OK] All dependencies installed."
