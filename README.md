# osint


cd /home/kali && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && \
# All Breach & Deep Search Tools
python3 -m pip install --user --break-system-packages --upgrade colorama requests[socks] holehe maigret sherlock social-analyzer h8mail && \
# Tor Service for Deepweb scraping
sudo apt update && sudo apt install tor -y && sudo service tor start && \
# Blackbird Setup (Powerful Username Search)
[ -d "tools/blackbird" ] || git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird && \
python3 -m pip install -r tools/blackbird/requirements.txt --user --break-system-packages && \
chmod +x khalid-osint.py && python3 khalid-osint.py
