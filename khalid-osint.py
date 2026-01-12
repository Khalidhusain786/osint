import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread, Lock
from stem import Signal
from stem.control import Controller

# Telegram Library
try:
    from telethon import TelegramClient, events
except ImportError:
    pass

init(autoreset=True)
all_raw_findings = []
print_lock = Lock()

# --- CONFIG ---
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'

# SOCKS5H ensures DNS is resolved by the Tor Exit Node, NOT your local ISP (No DNS Leak)
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def renew_tor_ip():
    """Control Port logic to change identity and avoid IP bans/empty results"""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="khalid_osint") # Make sure to set this in torrc
            controller.signal(Signal.NEWNYM)
            time.sleep(2)
        return True
    except:
        return False

def start_tor():
    # Check if Tor is running, if not start it
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start > /dev/null 2>&1")
        time.sleep(3)
    
    # Check Control Port 9051
    if renew_tor_ip():
        print(f"{Fore.GREEN}[OK] Stealth Identity: ACTIVE (Control Port 9051)")
    else:
        print(f"{Fore.YELLOW}[!] Warning: Control Port 9051 locked. Using standard Tor.")
    
    print(f"{Fore.GREEN}[OK] Ghost Engine: ONLINE (DNS Leak Protected)")

def dark_web_crawler(target, report_file):
    """V61: Deep Onion Crawling with DNS Protection"""
    onion_engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"http://haystak5njsu5hk.onion/search.php?q={target}",
        f"http://torchdeok6i7pud6x26sh6f4j6pqqhsk2fsit54v35ulswp7xmg6yd.onion/search?query={target}"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0'}
    
    for url in onion_engines:
        try:
            # Tor proxy usage with session to maintain DNS integrity
            session = requests.Session()
            session.proxies = proxies
            res = session.get(url, headers=headers, timeout=45)
            
            # Clean extraction logic
            matches = re.findall(r"([a-z2-7]{16,56}\.onion|password:\s?\S+|email:\s?\S+)", res.text, re.I)
            
            if matches or target.lower() in res.text.lower():
                with print_lock:
                    output = f"[DARK-WEB] Intel Found on: {url[:35]}..."
                    print(f"{Fore.RED}{output}")
                    all_raw_findings.append(output)
                    with open(report_file, "a") as f:
                        f.write(f"[DARK-WEB] Match in {url}\n")
        except:
            pass

def run_local_tool(cmd, name, report_file):
    """Reliable local tool runner with silent error handling"""
    try:
        # Using torsocks to force local tools through Tor as well
        secure_cmd = f"torsocks {cmd}"
        process = subprocess.Popen(secure_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            clean = line.strip()
            if any(x in clean.lower() for x in ["http", "found", "user", "@", "ip:"]):
                if not any(bad in clean.lower() for bad in ["searching", "checking", "trying"]):
                    with print_lock:
                        print(f"{Fore.GREEN}[FOUND] {Fore.YELLOW}{name}: {Fore.WHITE}{clean}")
                        all_raw_findings.append(clean)
                        with open(report_file, "a") as f: f.write(f"[{name}] {clean}\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║   KHALID OSINT - GHOST ENGINE (DNS PROTECTED) v61.0        ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/Username): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Launching Multi-Threaded Engine
    threads = [
        Thread(target=dark_web_crawler, args=(target, report_path)),
        Thread(target=run_local_tool, args=(f"sherlock {target}", "Sherlock", report_path)),
        Thread(target=run_local_tool, args=(f"maigret {target} --timeout 20", "Maigret", report_path))
    ]

    for t in threads: t.start()
    for t in threads: t.join()

    print(f"\n{Fore.GREEN}[➔] Ghost Scan Complete. Found: {len(all_raw_findings)} results.")

if __name__ == "__main__":
    main()
