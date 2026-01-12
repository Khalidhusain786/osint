# 🛡️ KHALID SHADOW BUREAU (v72.0)
**AI-Precision Indian Intelligence & Deep-Web OSINT Engine**



KHALID-OSINT ek advanced intelligence tool hai jo specifically **Indian Identity Verification** aur **Deep-Web Data Extraction** ke liye banaya gaya hai. Ye tool automatically underground mirrors, paste sites, aur social media networks ko scan karke target ka "Verified Data" nikalta hai.

---

## 🚀 Main Features
* **Precision AI Mode:** BeautifulSoup aur LXML integration se HTML kachra (tags) saaf karke sirf "Human-Readable" text dikhata hai.
* **Indian Identity Filter:** PAN Card, Voter ID, Vehicle RC (RTO), aur Aadhaar patterns ko automatically detect aur extract karta hai.
* **Stealth Browsing:** Pura intelligence scan **Tor Network** (Ghost Tunnel) ke peeche chalta hai, jisse aapka asli IP hamesha hidden rehta hai.
* **Multi-Tool Synergy:** Ek hi platform par **Sherlock, Maigret, aur Social-Analyzer** ka power use karke 1000+ social sites scan karta hai.
* **Clean Reporting:** Har scan ka accurate data `/reports/[target].txt` mein automatic save hota hai.

---

## 🛠️ Installation (Kali Linux / Ubuntu)



Apne terminal mein ye command chalao `/home/kali` ke liye:

```bash
# Repo clone karein aur home directory mein set karein
cd /home/kali
git clone [https://github.com/Khalidhusain786/osint.git](https://github.com/Khalidhusain786/osint.git)
cd osint

# Permissions de kar auto-installer run karein
chmod +x install.sh
sudo ./install.sh

### 🏁 HOW TO USE (STEP-BY-STEP)

    [!TIP] Follow these steps to operate the intelligence engine successfully:

1️⃣ Step One: Launch the Engine

Open your terminal and execute the main script:

python3 khalid-osint.py

2️⃣ Step Two: Input Target Data

When prompted ❯❯ Enter Target, you can input:

    Target Name: (e.g., Rahul Sharma) to find social profiles and database leaks.

    Username: (e.g., khalidhusain786) for deep social media footprinting.

    Identity Data: <kbd>ABCDE1234F</kbd> (PAN) or <kbd>9876543210</kbd> (Mobile).

3️⃣ Step Three: Analyze Results

The engine will display findings in real-time. Look for the Yellow Highlights in the terminal which indicate AI-Verified Matches.
4️⃣ Step Four: View Reports

All gathered intelligence is automatically saved here: cd /home/kali/osint/reports/
⚙️ Core Logic Engine

This script utilizes multi-threading and Tor-proxying to ensure speed and anonymity.

# Core Identification Regex Used by AI Engine
SURE_HITS = [
    r"[A-Z]{5}[0-9]{4}[A-Z]{1}",            # PAN Card
    r"[A-Z]{3}[0-9]{7}",                    # Voter ID
    r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}", # Vehicle RC
    r"(?:\+91|0)?[6-9]\d{9}"                # Indian Mobile
]

# AI Extraction utilizes BeautifulSoup for deep-clean scraping
# All traffic is forced through SOCKS5 proxy (Port 9050)

⚠️ Disclaimer

Educational and Ethical Use Only. This software is provided strictly for authorized OSINT investigations and educational research. Accessing private data without explicit consent or performing unauthorized surveillance is a violation of privacy laws and is strictly illegal. The developer, Khalid Husain, assumes no liability and is not responsible for any misuse, legal consequences, or damages resulting from the use of this tool. Use responsibly and stay within legal boundaries.

Developed by Khalid Husain
