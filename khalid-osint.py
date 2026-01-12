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
    """Tor service logic (v1-v42 Legacy Integrated)"""
    if os.system("systemctl is-active --quiet tor") != 0:
        print(f"{Fore.CYAN}[!] Deep-Web Access ke liye Tor start ho raha hai...")
        os.system("sudo service tor start")
        time.sleep(2)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def dark_web_mega_engine(target, report_file):
    """
    V43 Naya Module: Dark Web aur Deep Web ke saare links add kiye hain.
    Ek bhi purana engine delete nahi hua hai.
    """
    print(f"{Fore.MAGENTA}[*] Deep & Dark Web Scanning: Onion, I2P, & Hidden Wiki Archives...")
    
    # Powerful Darkweb & Deep Web Search Engines
    dark_engines = [
        f"https://ahmia.fi/search/?q={target}",                   # Surface-to-Tor portal
        f"https://duckduckgogg42xjoc72x3sja7o784uuy6qzrn6qzrn6qzrn.onion/html?q={target}", # DDG Onion
        f"http://jnv3gv3y6v63shl3.onion/search/{target}",         # Candle Search
        f"http://zqls36ky0.onion/wiki/index.php?search={target}", # Hidden Wiki Search
        f"http://phobos84.onion/search.php?q={target}",           # Phobos Search
        f"http://torch.onion/search?q={target}",                   # TORCH Engine
        f"https://www.google.com/search?q=site:onion.ly+%22{target}%22", # Deep Web Proxy
        f"https://www.google.com/search?q=site:onion.ws+%22{target}%22"  # Deep Web Proxy
    ]

    # Proxies for Tor access
    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}

    for url in dark_engines:
        try:
            # SOCKS5 proxy use karega taaki onion sites khul saken
            res = requests.get(url, proxies=proxies, timeout=15)
            # Onion address aur leaked patterns dhoondhna
            onions = re.findall(r'[a-z2-7]{16,56}\.onion', res.text)
            if onions:
                with open(report_file, "a") as f:
                    for onion in list(set(onions)):
                        print(f"{Fore.RED}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.RED}[DARK-WEB FOUND]: {Fore.WHITE}{onion}")
                        f.write(f"[DARK-WEB] {onion}\n")
                        found_data_for_pdf.append(f"[DARK-WEB] {onion}")
        except:
            pass

def verify_link(url):
    """Verification Logic: Fake data hatane ke liye (v39-v42 logic)"""
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        return r.status_code == 200
    except: return False

def run_tool_verified(cmd, name, report_file):
    """V1-V43: Sabhi tools ki execution lines intact hain."""
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
                elif any(x in clean_line.lower() for x in ["password:", "aadhar:", "voter:", "name:", "dob:"]):
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
    print(f"{Fore.RED}║    KHALID OSINT - DARK & DEEP WEB MASTER v43.0             ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (User/Email/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start Background Darkweb Scanning
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

    print(f"{Fore.BLUE}[*] Surface, Deep, & Dark Web Scans Active... NO LINE DELETED:\n")
    threads = [Thread(target=run_tool_verified, args=(cmd, name, report_path)) for cmd, name in tools]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"\n{Fore.GREEN}[➔] Done! Sab pichla data + Dark Web links add kar diye gaye hain.")

if __name__ == "__main__": main()
