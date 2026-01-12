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

def onion_intelligence_engine(target, report_file):
    """
    V49 Naya Module: Onion Search Engines & Darknet Leaks.
    Targets: Ahmia, Torch, Haystak, DarkDump, Cybercrime Forums.
    """
    print(f"{Fore.MAGENTA}[*] Deep Darknet Crawling: Searching Onion Land & Cybercrime Forums...")
    
    # List of Integrated Darkweb Search Nodes & Mirrors
    onion_targets = [
        f"https://ahmia.fi/search/?q={target}", 
        f"http://hss3uro2hsxfogfq.onion/search?q={target}", # Not Evil
        f"http://haystak5njsu5hk.onion/search.php?q={target}", # Haystak
        f"http://torch-search.onion/search?q={target}", # Torch
        f"http://onionland7v3un.onion/search?q={target}", # OnionLand
        f"http://darkeye6h7at.onion/query?q={target}", # DarkEye
        f"http://leaks-indexer.onion/search?id={target}" # OnionLeaks/Breach
    ]

    for url in onion_targets:
        try:
            # SOCKS5h use karke onion sites scan
            res = requests.get(url, proxies=proxies, timeout=20)
            # Onion links and sensitive leaks extract karna
            links = re.findall(r'[a-z2-7]{16,56}\.onion', res.text)
            if links:
                with open(report_file, "a") as f:
                    for link in list(set(links)):
                        print(f"{Fore.RED}[DARK-FOUND] Onion Link: {Fore.WHITE}http://{link}")
                        f.write(f"[ONION-INTEL] http://{link}\n")
                        all_raw_findings.append(f"Onion Leak: {link}")
        except:
            pass

def ai_summarizer_engine():
    if not all_raw_findings: return
    print(f"\n{Fore.MAGENTA}╔══════════════════════════════════════════════════════╗")
    print(f"{Fore.MAGENTA}║      AI DARKNET & BREACH SUMMARY (v49.0)             ║")
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
                
                # Link Verification
                match = re.search(r'(https?://\S+)', clean_line)
                if match:
                    url = match.group(1).rstrip(']').rstrip(')')
                    try:
                        r = requests.head(url, timeout=2)
                        if r.status_code == 200:
                            is_found = True
                            found_val = url
                    except: pass
                
                # Triggers for Credential/Breach/Forum Data
                elif any(x in clean_line.lower() for x in ["password:", "breach:", "market:", "forum:", "carding:", "leaked:"]):
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
    print(f"{Fore.RED}║    KHALID OSINT - DARKNET SOVEREIGN v49.0                  ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/Username/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start Darknet Engine in background
    Thread(target=onion_intelligence_engine, args=(target, report_path)).start()

    # LEGACY TOOLS (Zero Deletion)
    tools = [
        (f"h8mail -t {target} -q", "Credential-Breach"),
        (f"python3 -m blackbird -u {target}", "Market-Intel"),
        (f"maigret {target} --timeout 20", "Forum-Crawler"),
        (f"sherlock {target} --timeout 15 --print-found", "Handle-Tracker"),
        (f"holehe {target} --only-used", "Epieos-Intel")
    ]

    print(f"{Fore.BLUE}[*] Parallel Surface & Darknet Search Active... NO DATA DELETED\n")
    threads = [Thread(target=run_tool_strict_found, args=(cmd, name, report_path)) for cmd, name in tools]
    for t in threads: t.start()
    for t in threads: t.join()

    ai_summarizer_engine()
    print(f"\n{Fore.GREEN}[➔] Process Complete. Full Darknet Log: {report_path}")

if __name__ == "__main__":
    main()
