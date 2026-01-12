import os, subprocess, sys
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def run_tool(cmd, name, report_file):
    """Output ko real-time monitor karke save karega"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                if any(x in clean_line.lower() for x in ["http", "found", "[+]", "target", "user", "link"]):
                    print(f"{Fore.CYAN}[{name}] {Fore.WHITE}{clean_line}")
                    f.write(f"{name}: {clean_line}\n")
        process.wait()
    except Exception:
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.RED}KHALID OSINT - ORDERED SCAN MODE")
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    if not target: return

    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # Sequence updated: Social Analyzer first, PhoneInfoga last
    tools = [
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"), # Sabse Pehle
        (f"sherlock {target} --timeout 5", "Sherlock"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"photon -u {target}", "Photon"),
        (f"phoneinfoga scan -n {target}", "PhoneInfo") # Sabse Aakhiri
    ]

    print(f"{Fore.BLUE}[*] Starting Scan... Target: {target}\n")
    
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n{Fore.YELLOW}[➔] Scan Complete. File: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
