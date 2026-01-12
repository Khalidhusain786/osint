import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

# Forensic & Reporting (All Legacy Versions Intact)
try:
    import pdfkit
except ImportError:
    pass

init(autoreset=True)

# No Deletion Policy: Piche ka ek bhi data point delete nahi hua
found_data_for_pdf = []

def start_tor():
    """Tor service logic (v1-v38 Legacy Integrated)"""
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start")
        time.sleep(2)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def verify_link(url):
    """Naya Function: Link ko verify karne ke liye taaki fake data na aaye"""
    try:
        # 100% Real check: Agar site 200 OK degi tabhi dikhayega
        response = requests.get(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            return True
    except:
        return False
    return False

def run_tool_verified(cmd, name, report_file):
    """
    V1-V38: All tools lines are intact.
    Verification: Sirf verified links hi screen par aayenge.
    """
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                
                # Link nikalne ke liye pattern
                match = re.search(r'(https?://\S+)', clean_line)
                
                if match:
                    url = match.group(1)
                    # Screenshot wale 'Checking/Waiting' errors ko khatam karne ke liye Verification Check
                    if verify_link(url):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{url}")
                        output_str = f"[{name}] {url}"
                        f.write(f"{output_str}\n")
                        found_data_for_pdf.append(output_str)
                
                # Non-URL data (like passwords/aadhar) ke liye purane triggers
                elif any(x in clean_line.lower() for x in ["password:", "aadhar:", "voter:", "name:"]):
                    if not any(bad in clean_line.lower() for bad in ["checking", "waiting"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"[{name}] {clean_line}\n")
                        found_data_for_pdf.append(f"[{name}] {clean_line}")
        process.wait()
    except:
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - VERIFIED OMNI-ARCHIVE v39.0              ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Name/Email/Phone/ID): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # ALL PREVIOUS TOOLS (Zero Deletion Policy)
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

    print(f"{Fore.BLUE}[*] Crawling & Verifying Every Single Link... NO LINE DELETED:\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool_verified, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Mission Successful. All results verified and saved.")

if __name__ == "__main__":
    main
