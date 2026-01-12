import os, subprocess, sys, requests, re, time
from colorama import Fore, init
from threading import Thread

# Forensic & Reporting (All Versions Preserved)
try: import pdfkit
except: pass

init(autoreset=True)
found_data_for_pdf = []
all_raw_findings = [] 

def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo service tor start")
        time.sleep(2)
    print(f"{Fore.GREEN}[OK] Tor Connection: ACTIVE")

def ai_summarizer_engine():
    if not all_raw_findings:
        print(f"\n{Fore.RED}[!] No specific intelligence points found for AI summary.")
        return
    print(f"\n{Fore.MAGENTA}╔══════════════════════════════════════════════════════╗")
    print(f"{Fore.MAGENTA}║           AI INTELLIGENCE FINAL SUMMARY              ║")
    print(f"{Fore.MAGENTA}╚══════════════════════════════════════════════════════╝")
    unique_data = list(dict.fromkeys(all_raw_findings))
    for i, data in enumerate(unique_data[:20], 1):
        print(f"{Fore.WHITE}{i}. {data}")

def run_tool_strict_found(cmd, name, report_file):
    """
    Logic: 
    1. Screen par sirf FOUND data aayega.
    2. File mein SAB KUCH save hoga (No data loss).
    """
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        with open(report_file, "a") as f:
            f.write(f"\n--- {name} Full Log Start ---\n")
            
            for line in process.stdout:
                clean_line = line.strip()
                if not clean_line: continue
                
                # Sab kuch file mein save ho raha hai (Backup)
                f.write(f"{clean_line}\n")
                
                # --- SCREEN FILTER LOGIC ---
                is_found = False
                found_val = ""

                # 1. URL Check & Verification
                match = re.search(r'(https?://\S+)', clean_line)
                if match:
                    url = match.group(1).rstrip(']').rstrip(')')
                    # Sirf 200 OK links screen par
                    try:
                        r = requests.head(url, timeout=2, allow_redirects=True)
                        if r.status_code == 200:
                            is_found = True
                            found_val = url
                    except: pass
                
                # 2. Text Trigger Check (Aadhar, Passwords, etc.)
                elif any(x in clean_line.lower() for x in ["password:", "aadhar:", "voter:", "name:", "dob:", "location:", "match:"]):
                    # Negative filter taaki faltu lines screen par na aayein
                    if not any(bad in clean_line.lower() for bad in ["checking", "waiting", "not found", "no match", "searching"]):
                        is_found = True
                        found_val = clean_line

                # Sirf positive results hi print honge
                if is_found:
                    print(f"{Fore.GREEN}[FOUND] {Fore.YELLOW}{name}: {Fore.WHITE}{found_val}")
                    found_data_for_pdf.append(f"[{name}] {found_val}")
                    all_raw_findings.append(found_val)

            f.write(f"--- {name} Full Log End ---\n")
        process.wait()
    except Exception as e:
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - STRICT AI MASTER v47.0 (NO GARBAGE)      ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (User/Email/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Sabhi purane tools (v1-v46)
    tools = [
        (f"h8mail -t {target} -q", "Breach-Hunter"),
        (f"holehe {target} --only-used", "Email-Lookup"),
        (f"maigret {target} --timeout 20", "Identity-Mapper"),
        (f"python3 -m blackbird -u {target}", "Blackbird-Intel"),
        (f"sherlock {target} --timeout 15 --print-found", "Sherlock-Pro"),
        (f"truecallerpy search --number {target}", "Truecaller-Identity")
    ]

    print(f"{Fore.BLUE}[*] Deep Scan Running... Only confirmed data will be displayed.\n")
    
    threads = [Thread(target=run_tool_strict_found, args=(cmd, name, report_path)) for cmd, name in tools]
    for t in threads: t.start()
    for t in threads: t.join()

    ai_summarizer_engine()
    
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Process Complete.")
    print(f"{Fore.CYAN}[➔] Full Log Saved (Background): {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
