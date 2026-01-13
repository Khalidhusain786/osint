<h1 align="center">🕵️‍♂️ KHALID HYBRID OSINT ENGINE</h1>
<p align="center">
<b>Surface + Deep + Dark Recon • Telegram • Data Breaches • Onion Spider • Identity Extractor</b>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Recon-OSINT-blue?style=for-the-badge">
<img src="https://img.shields.io/badge/Mode-HYBRID-orange?style=for-the-badge">
<img src="https://img.shields.io/badge/Tor-AUTO-green?style=for-the-badge">
<img src="https://img.shields.io/badge/Report-TXT%2FPDF-yellow?style=for-the-badge">
<img src="https://img.shields.io/badge/Platform-Kali%20%7C%20Ubuntu%20%7C%20Termux-red?style=for-the-badge">
</p>

---

## 🚀 **About The Engine**

> **Khalid Hybrid OSINT Engine** is a full-spectrum recon suite that performs:
✔ Surface Web  
✔ Deep Web  
✔ Dark Web  
✔ Telegram Dorks  
✔ Leak Databases  
✔ Identity Extraction  
✔ Breach Checks  
✔ Final Reports  

All through one unified pipeline.

---

## 🧬 **Core Abilities**

✔ Automatic TOR routing (No manual start)  
✔ Deep + Dark onion spider gateways  
✔ Telegram intelligence dorks  
✔ Leak databases enumeration  
✔ Data breach hunter  
✔ WHOIS & platform lookups  
✔ Entity Identity Classification (PAN, Aadhaar, Phone, Address etc.)  
✔ PDF & TXT reporting  
✔ Artifact link retention  
✔ Colorized output  
✔ Threaded high-speed mode  

---

## 🔍 **Supported Targets**

```
Name
Email
Phone
PAN
Aadhaar
Voter ID
Domain
Username
Address Patterns
Bitcoin Wallets
IP & Network
```

---

## 🧩 **Recon Modules**

| Module | Layer |
|---|---|
| HTTP Dorks | Surface |
| Telegram Dorks | Semi-Deep |
| Pastebin/Leak Dumps | Deep |
| Onion Spider | Deep/Dark |
| Breach Check | LeakNet |
| Sherlock | Surface OSINT |
| Maigret | Aggregated OSINT |
| Identity Extraction | NLP |
| PDF Builder | Reporting |
| Tor Router | Transport |

---

## 🛠 **Installation**

### **Kali / Ubuntu / Parrot / Debian**

```bash
cd /home/kali && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && chmod +x install.sh && ./install.sh
```

### **Termux**

```bash
cd $HOME && pkg update -y && pkg upgrade -y && pkg install python git tor libxml2 libxslt clang make -y || (sudo apt update && sudo apt install -y python3 python3-pip git tor torsocks libxml2-dev libxslt-dev build-essential) && rm -rf osint && git clone https://github.com/Khalidhusain786/osint.git && cd osint && pip install --upgrade pip && pip install -r requirements.txt && chmod +x * && ([ -f khalid-osint.py ] && mv khalid-osint.py main.py || echo "File Ready"); python3 main.py
```

---

## ▶ **Run**

Direct launch:

```bash
python3 khalid-osint.py
```

---

## 🎛 **AUTO-TOR Mode**

✔ Automatically starts TOR  
✔ Applies onion socks proxy  
✔ No manual config required  

---

## 📁 **Folder Layout**

```
osint/
 ├─ khalid-osint.py
 ├─ install.sh
 ├─ requirements.txt
 ├─ api_keys.json
 ├─ reports/
 ├─ assets/
 │   └─ banner.png
 └─ screenshots/
```

---

## 📜 **Report Output**

Formats:

```
/reports/<target>.txt
/reports/<target>.pdf
```

Includes:

✔ Found Data  
✔ Sources  
✔ Dork hits  
✔ Onion links  
✔ Platform profiles  
✔ Evidence chain  

---

## 📸 **Screenshots**

```
screenshots/terminal.png
screenshots/report.png
```

(Will be auto added)

---

## 🔑 **Optional API Keys**

`api_keys.json`

```json
{
  "truecaller": "",
  "hunter": "",
  "email_hippo": "",
  "hlr_lookup": ""
}
```

---

## ⚡ Performance Notes

✔ Multi-threaded  
✔ Proxy aware  
✔ Timeout hardened  
✔ Onion fallback  
✔ Leak redundancy  

---

## 🧾 **Legal Notice**

> This tool is intended for **education + investigative OSINT** only.  
> User assumes all liability.  
> Do not violate privacy or local laws.

---

## 👑 **Author**

**Developer:** `Khalid Husain`  
**Engine:** `Hybrid Recon AI v1`

---

## 📜 **License**

```
MIT License
```

---

## ⭐ **Give it a Star**

If this helps your work, star the repo 🙂```

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
