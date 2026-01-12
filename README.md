# osint


cd /home/kali/osint && \
# 1. System dependencies update (No data deletion)
sudo apt-get update --fix-missing && \
sudo apt install -y tor libimage-exiftool-perl wkhtmltopdf python3-pip git colorama && \
# 2. Pip conflicts resolution for theHarvester and others
python3 -m pip install --user --break-system-packages --ignore-installed requests[socks] colorama beautifulsoup4==4.13.4 lxml==6.0.0 jinja2 pdfkit holehe maigret sherlock h8mail truecallerpy && \
# 3. Restoring tools directories
[ -d "tools/Photon" ] || git clone https://github.com/s0md3v/Photon.git tools/Photon && \
[ -d "tools/blackbird" ] || git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird && \
# 4. Starting service and running tool
sudo service tor start && python3 khalid-osint.py
