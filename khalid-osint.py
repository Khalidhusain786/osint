import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def start_tor():
    """Tor service ko automatically check aur start karega"""
    print(f"{Fore.YELLOW}[*] Checking Tor Service...")
    status = os.system("systemctl is-active --quiet tor")
    if status != 0:
        print(f"{Fore.CYAN}[!] Tor is inactive. Starting it now...")
        os.system("sudo service tor start")
        time.sleep(2) # Service start hone ka intezar
    print(f"{Fore.GREEN}[OK] Tor Service is Active.")

def search_breach_logs(target, report_file):
    """Deep search for leaks in Pastebin & Ahmia (Darkweb)"""
    print(f"{Fore.MAGENTA}[*] Checking Data-Breach Logs & Darkweb Archives...")
    ahmia_url = f"https://ahmia.fi/search/?q={target}"
    try:
        # Ahmia dorking
        res = requests.get(ahmia_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        leaks = re.findall(r'[a-z2-7]{16,56}\.onion', res.text)
        if leaks:
            with open(report_file, "a") as f:
                for leak in list(set(leaks)):
                    print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                    print(f"{Fore.RED}[BREACH/ONION] {Fore.WHITE}http://{leak}")
                    f.write(f"Darkweb Leak: http://{leak}\n")
    except: pass

def run_tool(cmd, name, report_file):
    try:
        # Errors ko bypass karne ke liye DEVNULL use kiya gaya hai
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # TELEGRAM BOT STYLE: Jo aapke screenshot mein hai
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "location:"]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    if not os.path
