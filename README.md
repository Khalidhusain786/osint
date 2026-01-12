# osint


# 1. Repositories fix karein taaki wkhtmltopdf mil sake
sudo apt-get update --fix-missing

# 2. Pip conflicts ko force-fix karein bina purana code touch kiye
python3 -m pip install --user --break-system-packages --ignore-installed beautifulsoup4==4.13.4 certifi==2025.7.14 lxml==6.0.0 requests==2.32.4 jinja2 pdfkit

# 3. Purane folders (Photon/Blackbird) ke conflicts handle karein
cd /home/kali/osint/tools && rm -rf Photon blackbird && cd ..

# 4. Tools ko fresh tareeke se restore karein (No Deletion Policy)
git clone https://github.com/s0md3v/Photon.git tools/Photon
git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird

# 5. Tool run karein
python3 khalid-osint.py
