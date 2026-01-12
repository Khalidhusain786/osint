import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

# Forensic aur PDF Save libraries (Safe & Intact)
try:
    from jinja2 import Template
    import pdfkit
except ImportError:
    pass

init(autoreset=True)

# No Deletion Policy: All historical data tracking
found_data_for_pdf = []

def start_tor():
    """Tor service auto-pilot - Logic from all previous versions"""
    if os.system("systemctl is-active --quiet tor") != 0:
        print(f"{Fore.CYAN}[!] Activating Tor Tunnel for Deep/Dark Web Crawling...")
        os.system("sudo service tor start")
        time.sleep(3)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def deep_intel_mega_engine_v35(target, report_file):
    """V1 to V34: Darkweb, Legal, PDF, Aadhar/Voter Dorks Merged"""
    engines = [
        f"https://ahmia.fi/search/?q={target}",
        f"https://www.google.com/search?q=site:onion.to+OR+site:onion.pet+%22{target}%22",
        f"https://www.google.com/search?q=%22{target}%22+filetype:pdf+voter+aadhar",
        f"https://www.google.com/search?q=%22{target}%22+password+leaked+OR+db+leak",
        f"https://www.google.com/search?q=site:gov.in+OR+site:nic.in+%22{target}%22",
        f"https://www.google.com/search?q=site:linkedin.com/in/+%22{target}%22",
        f"https://www.google.com/search?q=site:ecourts.gov.in+%22{target}%22"
    ]
    try:
        for url in engines:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, timeout=12, headers=headers)
            found_items = re.findall(r'[a-z2-7]{16,56}\.onion|[\w\.-]+@[\w\.-]+\.\w+', res.text)
            if found_items:
                with open(report_file, "a") as f:
                    for item in list(set(found_items)):
                        item_str = f"[DEEP-DISCOVERY] {item}"
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.RED}{item_str}")
                        f.write(f"{item_str}\n")
                        found_data_for_pdf.append(item_str)
    except: pass

def run_tool_final_archive(cmd, name, report_file):
    """V1-V34: Har tool ka execution bina kisi purani line ko hataye"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # All historical triggers merged (Surface to Forensic)
                triggers = [
                    "http", "found", "[+]", "password:", "address:", "father", "name:", "aadhar", 
                    "voter", "license", "pan", "dob:", "location:", "job:", "company:", "court:", "gps:", "lat:"
                ]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error", "searching"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        output_str = f"[{name}] {clean_line}"
                        f.write(f"{output_str}\n")
                        found_data_for_pdf.append(output_str)
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - THE ZERO-DELETION MASTER v35.0            ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (User/Email/Phone/ID): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start Background Intelligence Threads
    Thread(target=deep_intel_mega_engine_v35, args=(target, report_path)).start()

    # ALL TOOLS FROM V1 TO V34 (Sherlock to Truecaller)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter"),
        (f"holehe {target} --only-used", "Email-Lookup"),
        (f"maigret {target} --timeout 20", "Identity-Mapper"),
        (f"social-analyzer --username {target} --mode fast", "Social-Search"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"phoneinfoga scan -n {target}", "Phone-Intelligence"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"python3 tools/Photon/photon.py -u {target} --wayback", "Web-History"),
        (f"finalrecon --ss --whois --full {target}", "FinalRecon-Full"),
        (f"truecallerpy search --number {target}", "Truecaller-Identity")
    ]

    print(f"{Fore.BLUE}[*] Crawling All Historical Layers... SHOWING FOUND DATA ONLY:\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool_final_archive, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Investigation Complete. All v1-v34 Logic Preserved & Fixed.")

if __name__ == "__main__":
    main()
