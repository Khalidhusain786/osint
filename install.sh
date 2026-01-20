#!/bin/bash
# KHALID OSINT MASTER INSTALLER

echo "[+] Updating System & Installing PDF Libraries..."
sudo apt update
sudo apt install -y python3-venv python3-pip libpango-1.0-0 libpangoft2-1.0-0 libjpeg-dev libopenjp2-7-dev libffi-dev tor torsocks

echo "[+] Creating Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

echo "[+] Installing Python Modules..."
pip install --upgrade pip
pip install weasyprint markdown requests beautifulsoup4 colorama distro

echo "[+] Setup Complete!"
echo "To run the tool: source venv/bin/activate && python osint_v82.py 'target'"
