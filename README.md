# osint


# 1. Purana folder saaf karke naya download karein
cd ~ && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git

# 2. Folder mein jayein aur install karein
cd osint && chmod +x install.sh && ./install.sh

# 3. Tool chalayein
python3 khalid-osint.py

#Terminal mein ye paste karein taaki Desktop se ek click mein chale:

cat <<EOF > /root/Desktop/Khalid-OSINT.desktop
[Desktop Entry]
Name=Khalid OSINT
Exec=qterminal -e "bash -c 'cd /root/osint && python3 khalid-osint.py; exec bash'"
Icon=security-high
Terminal=true
Type=Application
EOF
chmod +x /root/Desktop/Khalid-OSINT.desktop
