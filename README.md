# osint


cd /home/kali && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && \
# Dependency conflicts bypass karke install karna
python3 -m pip install --user --break-system-packages --ignore-installed colorama requests[socks] holehe maigret sherlock social-analyzer h8mail && \
# Tor setup aur Blackbird fixed
sudo apt update && sudo apt install tor -y && \
[ -d "tools/blackbird" ] || git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird && \
python3 -m pip install -r tools/blackbird/requirements.txt --user --break-system-packages && \
chmod +x khalid-osint.py && python3 khalid-osint.py
