# osint


cd /home/kali && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && \
# Dependency conflicts fix aur saare tools install
python3 -m pip install --user --break-system-packages --ignore-installed colorama requests[socks] holehe maigret sherlock social-analyzer h8mail && \
# Photon (Web Intelligence) setup
[ -d "tools/Photon" ] || git clone https://github.com/s0md3v/Photon.git tools/Photon && \
# Blackbird (Advanced Social DB) setup
[ -d "tools/blackbird" ] || git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird && \
python3 -m pip install -r tools/blackbird/requirements.txt --user --break-system-packages && \
# Tor Service installation
sudo apt update && sudo apt install tor -y && sudo service tor start && \
chmod +x khalid-osint.py && python3 khalid-osint.py
