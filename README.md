# 1. Purani directory delete karein
rm -rf /home/kali/osint

# 2. Fresh clone karein
cd /home/kali
git clone https://github.com/Khalidhusain786/osint.git
cd osint

# 3. Permissions de kar installer chalaein
chmod +x install.sh
./install.sh

# 4. Engine launch karein
python3 khalid-osint.py
