# osint


# Tor aur SOCKS support install karein
sudo apt-get update --fix-missing
sudo apt-get install -y tor torsocks python3-pip

# Pip dependencies install karein (No deletion mode)
python3 -m pip install --user --break-system-packages --ignore-installed requests[socks] colorama beautifulsoup4 lxml jinja2 pdfkit

# Permission de kar installer run karein
chmod +x install.sh
sudo ./install.sh

# Final Tool Execution
python3 khalid-osint.py
