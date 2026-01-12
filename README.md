# osint


# 1. Tor aur SOCKS support install karein
sudo apt-get update --fix-missing
sudo apt-get install -y tor torsocks python3-pip

# 2. Pip dependencies for Darkweb scanning (No deletion)
python3 -m pip install --user --break-system-packages --ignore-installed \
requests[socks] colorama beautifulsoup4 lxml jinja2 pdfkit

# 3. Sab fix karke tool run karein
sudo service tor start && python3 khalid-osint.py
