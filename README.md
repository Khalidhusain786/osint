# 🛰️ **KHALID HYBRID OSINT ENGINE**

> **Surface + Deep + Dark Web OSINT Framework**  
> Auto PDF Export | Clickable Links | Multi‑Source Recon

---

## 🧰 **Features**
- 🔍 Sherlock Username Scan
- 📧 Email Breach Lookup
- 📱 Phone Intelligence (HLR + SIM + Country)
- 🔹 Telegram OSINT (Groups + Mentions)
- 🌑 Deep/Dark Web Query (.onion)
- 📑 Auto PDF Export (Clickable Links)
- 🕸 API Optional (Truecaller, HLR, Hunter, Hippo)
- 📦 One‑Click Installer
- 🎯 Works on **Kali + Termux**

---

## 📦 **Installation**

#### **Kali :**
```bash
sudo apt update
sudo apt install python3 python3-pip tor proxychains git -y
```

#### **Termux :**
```bash
pkg update
pkg install python git tor -y
```

---

## 🪂 **Clone**
```bash
git clone https://github.com/YourUser/Hybrid-OSINT.git
cd Hybrid-OSINT
```

---

## 📥 **Install Dependencies**
```bash
pip3 install -r requirements.txt
```

---

## 🚀 **Run**
```bash
python3 hybrid.py
```

---

## 📤 **Sample Output (PDF + Terminal)**

```text
[SHERLOCK] FOUND: github.com/rohit
[EMAIL-BREACH] LEAKED: 3 breaches
[TG-DATA] GROUP: t.me/cryptowatch
[DARK-DEEP] PASSPORT FOUND
[LINK] https://example.onion
```

> 📄 **PDF contains:**
✔ All data  
✔ All sources  
✔ Clickable links  
✔ Filename = Target Name  

---

## 🔑 **API Config (Optional)**

`config.json`
```json
{
  "truecaller": "",
  "hlr_lookup": "",
  "hunter": "",
  "email_hippo": ""
}
```

---

## 📸 **Screenshots**

> **Terminal:**
```
<img src="screens/terminal.png" width="600">
```

> **PDF Preview:**
```
<img src="screens/pdf.png" width="600">
```

> **Dashboard (optional future):**
```
<img src="screens/ui.png" width="600">
```

---

## 🛡️ **Legal**
For Educational, Research & Red‑Team Use Only.

---

### 👨‍💻 Author: **Khalid Husain**
