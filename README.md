# osint


# 1. Repositories ko reset aur update karein (Package not found fix)
sudo apt-get update --fix-missing

# 2. wkhtmltopdf aur system tools ko alag se install karein
sudo apt-get install -y tor libimage-exiftool-perl python3-pip git
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb || echo "Skipping manual download"
sudo apt install ./wkhtmltox_0.12.6-1.buster_amd64.deb -y || sudo apt install wkhtmltopdf -y

# 3. Pip conflicts ko bypass karke sare tools install karein
python3 -m pip install --user --break-system-packages --ignore-installed \
colorama==0.4.6 requests[socks] beautifulsoup4 lxml jinja2 pdfkit \
holehe maigret sherlock h8mail truecallerpy

# 4. Folder Conflicts Fix (Existing directory error bypass)
cd /home/kali/osint/tools && rm -rf Photon blackbird && cd ..
git clone https://github.com/s0md3v/Photon.git tools/Photon
git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird

# 5. Service start aur tool run
sudo service tor start && python3 khalid-osint.py
