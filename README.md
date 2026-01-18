```markdown
<p align="center">
  <img src="https://img.shields.io/badge/ELITE%20MARIANA%20COLLECTOR-v6.0-ff1744?style=for-the-badge&logo=tor&logoColor=white&labelColor=000000" alt="Version">
  <img src="https://img.shields.io/badge/Tor%20Network-Active-7B1FA2?style=for-the-badge&logo=tor&logoColor=white" alt="Tor">
  <img src="https://img.shields.io/badge/Playwright-Stealth%20Scraping-00D084?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/Pure%20Regex-No%20APIs-4CAF50?style=for-the-badge" alt="Pure Regex">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

<h1 align="center">💎 ELITE MARIANA COLLECTOR v6.0</h1>

<p align="center">
  <strong>Dark Web • Mariana Myth • Deep Market Stealth Scanner</strong><br>
  Tor + Playwright • Individual Items Printed on Screen • Pure Regex • No External APIs
</p>

<p align="center">
  <img src="https://via.placeholder.com/900x300/0D1117/FFFFFF?text=Elite+Mariana+Collector+v6.0+-+Dark+Intel+Suite" alt="Banner" width="900"/>
  <br><small>Custom banner daalne ke liye assets/banner.png upload karo</small>
</p>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Tor](https://img.shields.io/badge/Tor-Enabled-7B1FA2?style=flat-square&logo=tor&logoColor=white)](https://www.torproject.org/)

</div>

## 🔥 Features (Sab Add Kar Diye)

- 🕵️‍♂️ **Stealth Scraping** → Playwright Chromium + mouse simulation + scrolling + random delays
- 🔄 **Tor Circuit Rotation** → stem library (NEWNYM signal har baar)
- 📱 **Screen Par Har Item Print** → Vendors, Wallets (BTC/ETH), Emails, Phones, Domains, Drops – sab individually dikhte hain
- 🔍 **Pure Regex Extraction** → No API calls (Blockchair, Nominatim sab hata diye)
- 🌑 **Mariana Web Mode** + Real .onion markets support (list changeable)
- 💾 **Auto JSON Save** → iocs/{target}_mariana_results.json
- 📊 **Stylish Final Summary** → Counts ke saath separator lines
- ⚡ **Fast & Lightweight** → No heavy dependencies, no external services

## 📸 Terminal Output Demo (Yeh Dikhega)

```text
============================================================
🎯 TARGET: 7033635044
🌐 SOURCE: http://marianaonionxxx.onion
============================================================

👤 VENDORS FOUND (3):
 1. ShadowVendor
 2. EliteShopX
 3. DarkKing

💰 WALLETS FOUND (4):
 1. bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
 2. 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
 3. 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
 4. bc1qm34lsc65zpw79lxes69zkq26np2re8ndt5rt

📧 EMAILS FOUND (2):
 1. shadowvendor@protonmail.com
 2. elite@darkmail.com

📱 PHONES FOUND (1):
 1. +917896408248

🌐 DOMAINS FOUND (3):
 1. shadowmarket.cc
 2. eliteonion.ru
 3. darkdump.io

📦 DROPS FOUND (2):
 1. Patna Bihar India House No 45 Street 12
 2. Gaya Bihar Drop Point Near Railway Station

============================================================

🔥 FINAL ELITE SUMMARY 🔥
==================================================
🎯 TARGET: 7696408248
👥 VENDORS: 3
💰 WALLETS: 4
📧 EMAILS: 2
📱 PHONES: 1
🌐 DOMAINS: 3
📦 DROPS: 2
==================================================
```

## 🚀 Installation (One-Time – Kali Linux)

```bash
# Step 1: Update & Install basics
sudo apt update && sudo apt install -y \
    python3 python3-pip tor python3-stem \
    libnss3 libatk-bridge2.0-0 libxkbcommon0 libgbm1 libasound2

# Step 2: Python packages
pip3 install --upgrade pip
pip3 install aiohttp playwright stem requests pandas folium streamlit pyvis

# Step 3: Playwright browsers install
playwright install chromium --with-deps

# Step 4: Tor enable & restart
sudo systemctl enable tor
sudo systemctl restart tor

# Done!
```

## 🛠️ Run Karne Ka Tarika

```bash
python3 khalid-osint.py
```

Prompt aayega → target daalo (jaise 7696408248 ya koi keyword)

## 📂 Files Jo Banenge

```
iocs/
└── {target}_mariana_results.json   ← vendors, wallets, emails, phones, domains, drops sab save
```

## ⚠️ Important Warnings

- **Mariana Web real mein nahi hai** — yeh myth hai, listed .onion links fake hain (demo ke liye)
- Real darknet markets ke links **Dread forum** se lo (dread.onion search karo)
- **Legal Disclaimer**: Dark web scraping illegal activities ke liye use mat karo — jail ho sakti hai (India mein IT Act + NDPS)
- **Tor must be running** — check karo: `sudo service tor status`
- Educational / research purpose only

## 📜 License

MIT License — free to use, modify, share.

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with%20❤️%20by-Khalid%20Husain-red?style=for-the-badge&logo=heart&logoColor=white&labelColor=black" alt="Made with love">
</p>

<p align="center">
  <small>Patna, Bihar • January 2026</small>
</p>
```
