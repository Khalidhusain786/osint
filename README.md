# 🛰️ KHALID HYBRID OSINT ENGINE

> **Full-Spectrum Recon Framework**  
> Surface Web + Deep Web + Dark Web + Telegram + Breach DB + Identity & Phone + Export

---

## 🏷️ Status & Info

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Type](https://img.shields.io/badge/Engine-Hybrid%20OSINT-blue)
![Layer](https://img.shields.io/badge/Web%20Layers-Surface%20%2B%20Deep%20%2B%20Dark-black)
![Report](https://img.shields.io/badge/Export-PDF%20%2B%20TXT-orange)
![Language](https://img.shields.io/badge/Language-Python-yellow)
![Platform](https://img.shields.io/badge/Platform-Kali%20%7C%20Ubuntu%20%7C%20Termux-informational)

---

## 🎯 Mission

**OSINT — Hybrid Recon Engine (Surface + Deep + Dark)**  
Designed for investigators, red-teamers, analyst & cyber forensic tasks.

---

## ⚙️ Modules & Capabilities

✔ **Surface Layer**
- Sherlock / Maigret (username OSINT)
- Email OSINT
- Phone lookup
- Social enumerations
- Public Breach DB

✔ **Deep / Dark Layer**
- Onion crawling
- Marketplace lookup
- Dumps / DB breach artifacts
- Ghost relay for Dark requests

✔ **Identity & Number Intelligence**
- Phone
- WhatsApp metadata
- Telegram
- Truecaller (API optional)

✔ **Telegram Recon**
- Username / Mention / Group / Channel intel

✔ **Breach Dump Recon**
- Combo leaks
- Mail-pass dumps
- Credential search

✔ **Export**
- PDF
- TXT
- Terminal minimal hits

---

## 🧩 Architecture Tree

```
KHALID HYBRID OSINT ENGINE
├── Surface Recon
│   ├── Sherlock
│   ├── Maigret
│   ├── Email
│   ├── Phone
│   └── Breach DB
├── Deep Recon
│   ├── Breach Dumps
│   ├── DB Lookup
│   └── Dark Market
└── Dark Web
    ├── Tor Relay
    ├── Onion Support
    └── Ghost Tunnel
```

---

## 📦 Requirements

> Auto installed by script

- Python3
- pip
- tor (if dark web active)
- system packages

---

## 🚀 Installation + Run (One Line, Color)

**Just copy → paste → run**

```bash
cd /home/kali && rm -rf /home/kali/osint && echo -e "\033[1;32m[CLONING REPO]\033[0m" && git clone https://github.com/Khalidhusain786/osint.git && cd osint && echo -e "\033[1;33m[INSTALLING DEPENDENCIES]\033[0m" && chmod +x install.sh && ./install.sh && echo -e "\033[1;35m[LAUNCHING OSINT — Hybrid Recon Engine (Surface + Deep + Dark)]\033[0m" && python3 khalid-osint.py
```

---

## 🖥️ Output Preview

> **Minimal Terminal Output (Only Hits)**

```
[DARK-DEEP] Passport leak found
[TG-DATA] Mention detected: @username
[BREACH] Email found in 4 breaches
[LINK] https://example.onion
[REPORT] Saved → /reports/target.pdf
```

---

## 📑 Report System

Export options:

✔ Terminal Hits  
✔ PDF Report  
✔ TXT Raw  

All reports auto-saved using:

```
{target}/{target_report}.pdf
```

---

## 🔑 API Keys (Optional)

Place in:

```
config/api_keys.json
```

Supported:

- truecaller
- hunter
- emailhippo
- hlr lookup

---

## 📱 Platforms Supported

✔ Kali Linux  
✔ Ubuntu / Debian  
✔ Parrot OS  
✔ Termux (Android)  
✔ VPS / Cloud / Local

---

## ⚖️ Legal Disclaimer

This project is for **OSINT & Educational Forensics** only.  
User is responsible for usage compliant with law & jurisdiction.

---

## 👑 Credits

Author: **Khalid Husain**  
Engine: **Hybrid OSINT Recon**

---

## 📜 License

MIT License (safe for public use & fork)

---

## 🗺️ Roadmap (Future)

- Browser Fingerprint Recon
- Telegram Bots Integration
- Full GUI Panel
- Auto Enrichment
