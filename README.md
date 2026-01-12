# osint


cd /home/kali && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && \
python3 -m pip install --user --break-system-packages --upgrade colorama requests[socks] holehe sherlock maigret social-analyzer phoneinfoga && \
chmod +x khalid-osint.py && python3 khalid-osint.py
