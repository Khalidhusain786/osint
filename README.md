# osint


# 1. Sabse pehle purane broken packages fix karein
sudo apt-get update --fix-missing
python3 -m pip install --user --break-system-packages --ignore-installed beautifulsoup4==4.13.4 lxml==6.0.0 requests==2.32.4

# 2. Sherlock aur Maigret ko update karein taaki wo latest websites ko pehchan sakein
python3 -m pip install --upgrade sherlock maigret --break-system-packages

# 3. Tool run karein
python3 khalid-osint.py
