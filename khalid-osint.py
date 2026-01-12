import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

# Forensic & Reporting (Legacy All Preserved)
try:
    import pdfkit
except ImportError:
    pass

init(autoreset=True)

# No Deletion Policy: Piche ka ek bhi logic delete nahi hua
found_data_for_pdf = []

def start_tor():
    """Tor service logic (v1-v43 Legacy Integrated)"""
    if os.system("systemctl is-active --quiet tor") != 0:
        print(f"{Fore.CYAN}[!] Deep-Web & Telegram Intelligence ke liye Tor start ho raha hai...")
        os.system("sudo service tor start")
        time.sleep(2)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def telegram_intel_engine(target, report_file):
    """
    V44 Naya Module: Telegram Channels, Groups, aur Users scan karne ke liye.
    Ek bhi purana engine delete nahi hua hai.
    """
    print(f"{Fore.BLUE}[*] Telegram Intelligence Scanning: Searching Channels, Groups & Bios...")
    
    tg_engines = [
        f"https://lyzem.com/search?q={target}",
        f"https://telemetr.io/en/channels?search={target}",
        f"https://tgstat.com/search?q={target}",
        f"https://www.google.com/search?q=site:t.me+%22{target}%22",
        f"https://www.google.com/search?q=site:telegram.me+%22{target}%22"
    ]

    for url in tg_engines:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=10)
            # Telegram links (t.me/username) dhoondhna
            tg_links = re.findall(r't\.me/[\w\d_]+', res.text)
            if tg_links:
                with open(report_file, "a") as f:
                    for link in list(set(tg_links)):
                        clean_link = f"https://{link}"
                        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.CYAN}[TELEGRAM FOUND]: {Fore.WHITE}{clean_link}")
                        f.write(f"[TELEGRAM] {clean_link}\n")
                        found_data_for_pdf.append(f"[TELEGRAM] {clean_link}")
        except:
            pass

def dark_web_mega_engine(target, report_file):
    """V43 Darkweb Module (Intact)"""
    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    dark_engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"http://torch.onion/search?q={target}",
        f"http://jnv3gv3y6v63shl3.onion/search/{target}"
    ]
    for url in dark_engines:
        try:
            res = requests.get(url, proxies=proxies, timeout=15)
            onions = re.findall(r'[a-z2-7]{16,56}\.onion', res.text)
            if onions:
                with open(report_file, "a") as f:
                    for onion in list(set(onions)):
                        print(f"{Fore.RED}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.RED}[DARK-WEB FOUND]: {Fore.WHITE}{onion}")
                        f.write(f"[DARK-WEB] {onion}\n")
                        found_data_for_pdf.append(f"[DARK-WEB] {onion}")
        except: pass

def verify_link(url):
    """Verification Logic: v39-v43 logic (Intact)"""
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        return r.status_code == 200
    except: return False

def run_tool_verified(cmd, name, report_file):
    """V1-V44: Sabhi tools ki execution lines intact hain."""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                match = re.search(r'(https?://\S+)', clean_line)
                if match:
                    url = match.group(1).rstrip(']')
                    if verify_link(url):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.YELLOW}➤ {name}: {Fore.WHITE}{url}")
                        f.write(f"[{name}] {url}\n")
                        found_data_for_pdf.append(f"[{name}] {url}")
                elif any(x in clean_line.lower() for x in ["password:", "aadhar:", "voter:", "name:"]):
                    print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                    f.write(f"[{name}] {clean_line}\n")
                    found_data_for_pdf.append(f"[{name}] {clean_line}")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - THE ETERNAL TELEGRAM MASTER v44.0        ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (User/Email/Phone/Telegram_ID): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start Background Scanning (Telegram & Darkweb)
    Thread(target=telegram_intel_engine, args=(target, report_path)).start()
    Thread(target=dark_web_mega_engine, args=(target, report_path)).start()

    # ALL PREVIOUS TOOLS (Zero Deletion Policy)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter"),
        (f"holehe {target} --only-used", "Email-Lookup"),
        (f"maigret {target} --timeout 20", "Identity-Mapper"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"truecallerpy search --number {target}", "Truecaller-Identity")
    ]

    print(f"{Fore.BLUE}[*] Telegram, Darkweb & Surface Scans Active... NO LINE DELETED:\n")
    threads = [Thread(target=run_tool_verified, args=(cmd, name, report_path)) for cmd, name in tools]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"\n{Fore.GREEN}[➔] Done! Telegram links add ho gaye hain aur pichla data mehfooz hai.")

if __name__ == "__main__": main()
