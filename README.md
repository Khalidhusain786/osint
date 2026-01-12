# osint


# 1. Sabse pehle permissions aur directories fix karein
cd /home/kali/osint && chmod +x khalid-osint.py

# 2. Screenshot wale 'Package Not Found' errors ko fix karne ke liye repositories update
sudo apt-get update --fix-missing

# 3. Missing System Tools install karein (PDF aur Tor ke liye)
sudo apt install -y tor libimage-exiftool-perl wkhtmltopdf python3-pip git

# 4. Pip Conflicts (theHarvester/BeautifulSoup) ko fix karein - NO DELETION logic
python3 -m pip install --user --break-system-packages --ignore-installed \
requests[socks] colorama beautifulsoup4==4.13.4 lxml==6.0.0 jinja2 pdfkit \
holehe maigret sherlock h8mail truecallerpy

# 5. Tor service ko background mein start karein
sudo service tor start

# 6. Tool run karein
python3 khalid-osint.py
