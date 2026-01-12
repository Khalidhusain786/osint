# osint


cd /home/kali && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && \
# Base tools
python3 -m pip install --user --break-system-packages --upgrade colorama requests[socks] holehe sherlock maigret social-analyzer && \
# Blackbird (Powerful Username Search) manual fix
git clone https://github.com/p1ngul1n0/blackbird.git tools/blackbird && \
python3 -m pip install -r tools/blackbird/requirements.txt --user --break-system-packages && \
# PhoneInfoga fix
(command -v phoneinfoga >/dev/null || (curl -sSL https://raw.githubusercontent.com/sundowndev/phoneinfoga/master/support/install | bash && sudo mv ./phoneinfoga /usr/local/bin/)) && \
chmod +x khalid-osint.py && python3 khalid-osint.py
