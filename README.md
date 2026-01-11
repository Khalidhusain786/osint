# osint


rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git

cd osint && chmod +x install.sh && ./install.sh

python3 khalid-osint.py


#paste in terminal

cat <<EOF > ~/Desktop/Khalid-OSINT.desktop
[Desktop Entry]
Name=Khalid OSINT
Exec=qterminal -e "python3 $(pwd)/khalid-osint.py"
Icon=security-high
Terminal=true
Type=Application
EOF
chmod +x ~/Desktop/Khalid-OSINT.desktop
