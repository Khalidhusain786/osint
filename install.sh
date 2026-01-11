#!/bin/bash
# Developer: Khalid Husain (@khalidhusain786)
# Feature: Self-Healing & Auto-Dependency Fixer

echo -e "\e[1;32m[*] Khalid OSINT: Building Immortal Environment...\e[0m"

# Basic structure
mkdir -p reports/pdf reports/json reports/txt tools modules

# Installing core system requirements
sudo apt update && sudo apt install -y python3 python3-pip python3-full git curl wget

# Essential libraries (Force-install with break-system-packages for Kali compatibility)
pip install --upgrade pip --break-system-packages
pip install colorama requests phonenumbers fpdf flask pyfiglet holehe maigret --break-system-packages --ignore-installed

# Download core engines to local 'tools' folder to bypass system errors
cd tools
git clone --depth=1 https://github.com/sherlock-project/sherlock.git 2>/dev/null || (cd sherlock && git pull)
git clone --depth=1 https://github.com/soxoj/maigret.git 2>/dev/null || (cd maigret && git pull)
cd ..

chmod +x khalid-osint.py
echo -e "\e[1;34m[!] Setup Immortal! Ab 'python3 khalid-osint.py' chalaein.\e[0m"
