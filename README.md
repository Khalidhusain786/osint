# osint

# Home directory mein move karein aur purana setup saaf karein
cd /home/kali && rm -rf osint

# Repo clone karein aur dependencies install karein
git clone https://github.com/Khalidhusain786/osint.git && cd osint
sudo apt-get update && sudo apt-get install -y tor torsocks python3-pip nodejs npm

# Superfast AI parsing ke liye zaroori libraries
pip3 install beautifulsoup4 lxml requests[socks] colorama --break-system-packages

# Global OSINT tools setup
sudo npm install -g social-analyzer
pip3 install sherlock maigret --break-system-packages

# Installer ko permission de kar run karein
chmod +x install.sh
sudo ./install.sh
