import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

# Forensic & Reporting (Legacy All Preserved)
try: import pdfkit
except: pass

init(autoreset=True)
found_data_for_pdf = []

def verify_link(url):
    """Naya Verification Logic: Fake data (Checking/Waiting) hatane ke liye"""
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        return r.status_code == 200
    except: return False

def run_tool_final(cmd, name, report_file):
    """V1-V39: Ek bhi line delete nahi, sirf verified results filter"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Link dhundhna aur verify karna
                match = re.search(r'(https?://\S+)', clean_line)
                if match and verify_link(match.group(1)):
                    print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.YELLOW}➤ {name}: {Fore.WHITE}{match.group(1)}")
                    f.write(f"[{name}] {match.group(1)}\n")
                    found_data_for_pdf.append(f"[{name}] {match.group(1)}")
                # Piche ke saare purane triggers (Aadhar, Voter, Passwords)
                elif any(x in clean_line.lower() for x in ["password:", "aadhar:", "voter:", "name:", "dob:"]):
                    if not any(bad in clean_line.lower() for bad in ["checking", "waiting"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"[{name}] {clean_line}\n")
                        found_data_for_pdf.append(f"[{name}] {clean_line}")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    if os.system("systemctl is-active --quiet tor") != 0: os.system("sudo service tor start")
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - FINAL VERIFIED MASTER v39.0               ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target: ")
    report_path = os.path.abspath(f"reports/{target}.txt")

    # ALL TOOLS RESTORED (V1-V39 Zero Deletion)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter"),
        (f"holehe {target} --only-used", "Email-Lookup"),
        (f"maigret {target} --timeout 20", "Identity-Mapper"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"truecallerpy search --number {target}", "Truecaller-Identity")
    ]

    threads = [Thread(target=run_tool_final, args=(cmd, name, report_path)) for cmd, name in tools]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"\n{Fore.GREEN}[➔] Done! Sab data mehfooz hai: {report_path}")

if __name__ == "__main__": main()
