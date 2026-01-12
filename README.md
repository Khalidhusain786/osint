# osint


# Home directory mein move karein aur purana folder saaf karein
cd /home/kali && rm -rf osint

# Repo clone karein
git clone https://github.com/Khalidhusain786/osint.git && cd osint

# System updates aur core tools
sudo apt-get update && sudo apt-get install -y tor torsocks python3-pip nodejs npm

# Python libraries (Kali Linux ke naye rules ke mutabik)
python3 -m pip install --user --break-system-packages requests[socks] colorama beautifulsoup4 lxml jinja2 pdfkit sherlock maigret

# Social-Analyzer global install
sudo npm install -g social-analyzer

# Installer ko permission de kar run karein
chmod +x install.sh
sudo ./install.sh

cd /home/kali/osint && python3 khalid-osint.py
