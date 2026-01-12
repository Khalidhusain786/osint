import os, subprocess, sys
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def run_tool(cmd, name, report_file):
    """Glt data filter karne ke liye strict logic"""
    try:
        # stderr ko hide kiya taaki faltu warnings na dikhen
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                
                # False Positives filter karne ke liye keywords
                # Ye sirf tabhi print karega jab 'found', 'http' ya profile link milega
                bad_keywords = ["not found", "404", "error", "no results", "could not", "failed"]
                
                if any(x in clean_line.lower() for x in ["http://", "https://", "[+] found", "target:"]):
                    # Check karein ki line mein koi negative word toh nahi hai
                    if not any(bad in clean_line.lower() for bad in bad_keywords):
                        output = f"{Fore.GREEN}[VERIFIED] {Fore.CYAN}{name}: {Fore.WHITE}{clean_line}"
                        print(output)
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except:
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.RED}KHALID OSINT - VERIFIED DATA ONLY MODE")
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    if not target: return

    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # Fast flags add kiye hain taaki galat sites par time waste na ho
    tools = [
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock"),
        (f"maigret {target} --timeout 8 --no-recursion", "Maigret"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"photon -u {target} --wayback -l 1", "Photon"),
        (f"phoneinfoga scan -n {target}", "PhoneInfo")
    ]

    print(f"{Fore.BLUE}[*] Parallel Scan Active... Filtering False Positives.\n")

    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
