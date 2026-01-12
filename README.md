# osint


cd /home/kali && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && \
# Dependency conflicts fix (Force override)
python3 -m pip install --user --break-system-packages --ignore-installed colorama requests[socks] holehe maigret sherlock social-analyzer h8mail truecallerpy aiohttp==3.10.0 && \
# Tor setup
sudo apt update && sudo apt install tor -y && sudo service tor start && \
# Photon & Blackbird restore
[ -d "tools/Photon" ] || git clone https://github.com/s0md3v/Photon.git tools/Photon && \
[ -d "tools/blackbird" ] || git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird && \
python3 -m pip install -r tools/blackbird/requirements.txt --user --break-system-packages && \
chmod +x khalid-osint.py && python3 khalid-osint.py
