# osint


cd /home/kali/osint && \
# Installing reporting tools and fixing pip conflicts (No data loss)
python3 -m pip install --user --break-system-packages --ignore-installed colorama requests[socks] holehe maigret sherlock social-analyzer h8mail truecallerpy aiohttp==3.10.0 aiofiles==23.2.1 jinja2 pdfkit && \
# Tor and system dependencies
sudo apt update && sudo apt install tor libimage-exiftool-perl wkhtmltopdf -y && sudo service tor start && \
# Restoring old tools if missing
[ -d "tools/Photon" ] || git clone https://github.com/s0md3v/Photon.git tools/Photon && \
[ -d "tools/blackbird" ] || git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird && \
chmod +x khalid-osint.py && python3 khalid-osint.py
