import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

# Forensic & Reporting (Legacy All Preserved)
try: import pdfkit
except: pass

init(autoreset=True)
found_data_for_pdf = []
all_raw_findings = [] 

# TOR PROXY CONFIGURATION
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start")
        time.sleep(2)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def telegram_bot_intel_engine(target, report_file):
    """
    V50 Naya Module: Telegram Bot Data Scraper.
    Ye Telegram API portals aur public info bots ka data dhoondhega.
    """
    print(f"{Fore.BLUE}[*] Telegram Bot Intel: Scanning Leaked Bot Databases & Public Info...")
    
    # Telegram-specific web gateways jo bots ka data index karte hain
    tg_gateways = [
        f"https://search.intelligencex.tv/?s={target}", # IntelX Bot Mirror
        f"https://t.me/s/Osint_Bot_List?q={target}",    # Public Bot Logs
        f"https://telemetr.io/en/channels?search={target}", 
        f"https://lyzem.com/search?q={target}"
    ]

    for url in tg_gateways:
        try:
            res = requests.get(url, timeout=10)
            # Bot specific identifiers aur results dhoondhna
            bot_data = re.findall(r'(@[\w\d_]+bot|t\.me/[\w\d_]+)', res.text)
            if bot_data:
                with open(report_file, "a") as f:
                    for entry in list(set(bot_data)):
                        result = f"Potential Bot Match: {entry}"
                        print(f"{Fore.CYAN}[BOT-INTEL] {Fore.WHITE}{result}")
                        f.write(f"[TG-BOT-DATA] {result}\n")
                        all_raw_findings.append(result)
        except:
            pass

def onion_intelligence_engine(target, report_file):
    """V49 Darknet Module (Intact)"""
    onion_targets = [
        f"https://ahmia.fi/search/?q={target}", 
        f"http://torch-search.onion/search?q={target}",
        f"http://haystak5njsu5hk.onion/search.php?q={target}"
    ]
    for url in onion_targets:
        try:
            res = requests.get(url, proxies=proxies, timeout=15)
            links = re.findall(r'[a-z2-7]{16,56}\.onion', res.text)
            if links:
                with open(report_file, "a") as f:
                    for link in list(set(links)):
                        print(f"{Fore.RED}[DARK-FOUND] Onion Link: {Fore.WHITE}http://{link}")
                        f.write(f"[ONION-INTEL] http://{link}\n")
                        all_raw_findings.append(f"Onion Leak: {link}")
        except: pass

def ai_summarizer_engine():
    if not all_raw_findings: return
    print(f"\n{Fore.MAGENTA}╔══════════════════════════════════════════════════════╗")
    print(f"{Fore.MAGENTA}║      AI OMNI-INTELLIGENCE SUMMARY (v50.0)            ║")
    print(f"{Fore.MAGENTA}╚══════════════════════════════════════════════════════╝")
    for i, data in enumerate(list(dict.fromkeys(all_raw_findings))[:30], 1):
        print(f"{Fore.WHITE}{i}. {data}")

def run_tool_strict_found(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                if not clean_line: continue
                f.write(f"{clean_line}\n")
                
                is_found = False
                found_val = ""
                
                match = re.search(r'(https?://\S+)', clean_line)
                if match:
                    url = match.group(1).rstrip(']').rstrip(')')
                    try:
                        r = requests.head(url, timeout=2)
                        if r.status_code == 200:
                            is_found = True
                            found_val = url
                    except: pass
                elif any(x in clean_line.lower() for x in ["password:", "breach:", "name:", "bot:", "chat_id:"]):
                    if not any(bad in clean_line.lower() for bad in ["checking", "searching", "not found"]):
                        is_found = True
                        found_val = clean_line

                if is_found:
                    print(f"{Fore.GREEN}[FOUND] {Fore.YELLOW}{name}: {Fore.WHITE}{found_val}")
                    all_raw_findings.append(found_val)
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - BOT & DARKNET MASTER v50.0               ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/Username/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start Background Engines
    Thread(target=onion_intelligence_engine, args=(target, report_path)).start()
    Thread(target=telegram_bot_intel_engine, args=(target, report_path)).start()

    # LEGACY TOOLS (Zero Deletion)
    tools = [
        (f"h8mail -t {target} -q", "Credential-Breach"),
        (f"python3 -m blackbird -u {target}", "Social-Market-Intel"),
        (f"maigret {target} --timeout 20", "Deep-Forum-Crawler"),
        (f"sherlock {target} --timeout 15 --print-found", "Handle-Tracker"),
        (f"holehe {target} --only-used", "Epieos-Email-Intel")
    ]

    print(f"{Fore.BLUE}[*] Parallel Bot, Surface & Darknet Search Active...\n")
    threads = [Thread(target=run_tool_strict_found, args=(cmd, name, report_path)) for cmd, name in tools]
    for t in threads: t.start()
    for t in threads: t.join()

    ai_summarizer_engine()
    print(f"\n{Fore.GREEN}[➔] Done! Full Intelligence Log: {report_path}")

if __name__ == "__main__":
    main()
