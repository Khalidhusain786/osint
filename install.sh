#!/bin/bash
echo -e "\e[1;32m[*] Installing 360-Degree Global Search (Govt + Private + Hidden)...\e[0m"

# System Clean
sudo killall apt apt-get dpkg 2>/dev/null
sudo rm -rf /var/lib/dpkg/lock-frontend /var/lib/apt/lists/lock
sudo dpkg --configure -a

# Install Stable Tools
pip install colorama requests[socks] holehe maigret social-analyzer --break-system-packages --ignore-installed

# Start TOR for Dark Web
sudo apt update && sudo apt install tor proxychains4 -y
sudo service tor start

# Desktop Shortcut Creator
cat <<EOF > ~/Desktop/Khalid-OSINT.desktop
[Desktop Entry]
Name=Khalid OSINT
Exec=qterminal -e "python3 $(pwd)/khalid-osint.py"
Icon=security-high
Terminal=true
Type=Application
EOF
chmod +x ~/Desktop/Khalid-OSINT.desktop

echo -e "\e[1;34m[!] ALL DONE! Ab Desktop par Khalid-OSINT icon par click karein.\e[0m"
