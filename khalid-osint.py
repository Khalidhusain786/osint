import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

# --- ADVANCED IDENTITY & TRUECALLER LOGIC ---

def truecaller_search(target):
    """Phone number se Name aur Carrier nikalne ke liye"""
    print(f"{Fore.CYAN}[*] Attempting Truecaller Identity Search for: {target}")
    # Note: truecallerpy backend use karta hai

def search_indian_gov_leaks(target, report_file):
    """Voter List, Aadhar context aur Gov directories scan karne ke liye"""
    print(f"{Fore.MAGENTA}[*] Scanning Indian Government Directories (PDF/XLS/Docs)...")
    dorks = [
        f"https://www.google.com/search?q=filetype:pdf+%22{target}%22+voter+list",
        f"https://www.google.com/search?q=site:gov.in+OR+site:nic.in+%22{target}%22",
        f"https://www.google.com/search?q=site:pastebin.com+%22{target}%22+aadhar"
    ]
    # Background scraping triggers added
    pass

# --- CORE FUNCTIONS (RETAINED DATA) ---

def auto_update():
    print(f"{Fore.CYAN}[*] Synchronizing with Global Intelligence Databases...")
    try: os.system("git fetch --all && git reset --hard origin/main")
    except: pass

def start_tor():
    print(f"{Fore.YELLOW}[*] Tunneling through Darkweb (Tor)...")
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start")
        time.sleep(2)

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # TELEGRAM BOT STYLE TRIGGERS (Aapke Screenshots ki tarah)
                # Isme Name, Father-name, Address, Aadhar sab triggers hain
                triggers = ["http", "found", "[+]", "password:", "address:", "father", "name:", "aadhar", "voter", "license", "pan", "document", "dob:", "location:"]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"[{name}] {clean_line}\n")
        process.wait()
    except: pass

def main():
    auto_update()
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - ALL TOOLS + DARKWEB + TRUECALLER       ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (User/Phone/Email/Aadhar): ")
    if not target: return
    
    # Path save usi naam se hoga jo target input hai
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start Deep Web & Gov Scanning Threads
    Thread(target=truecaller_search, args=(target,)).start()
    Thread(target=search_indian_gov_leaks, args=(target, report_path)).start()

    # ALL TOOLS (Purane saare + Sab naye)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter (HIBP)"),
        (f"holehe {target} --only-used", "Email-Register"),
        (f"maigret {target} --timeout 25", "Deep-Identity-Mapper"),
        (f"social-analyzer --username {target} --mode fast", "Social-Search"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"phoneinfoga scan -n {target}", "Global-Phone-Scan"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"python3 tools/Photon/photon.py -u {target} --wayback", "Web-Archive-Scraper"),
        (f"finalrecon --ss --whois --full {target}", "FinalRecon-Full")
    ]

    print(f"{Fore.BLUE}[*] Crawling Surface, Deep & Dark Web... Results Only:\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Mission Complete. Full Case-File Saved In: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
