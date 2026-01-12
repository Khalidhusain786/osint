import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

def run_legacy_tool(cmd, name, report_file):
    """Sahi try-except logic taaki script break na ho"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ["http", "found", "[+]", "link:"]):
                    print(f"{Fore.CYAN}[+] {name}: {Fore.WHITE}{line.strip()}")
                    f.write(f"{name}: {line.strip()}\n")
    except Exception:
        # Syntax fix: except block ab missing nahi hai
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}KHALID OSINT - FULL RECOVERY MODE")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # Saare purane tools wapis active hain
    print(f"{Fore.BLUE}[*] Scanning all secondary modules...\n")
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer"),
        (f"blackbird -u {target}", "Blackbird")
    ]
    
    for cmd, name in tools:
        run_legacy_tool(cmd, name, report_path)
        
    print(f"\n{Fore.YELLOW}[➔] Process Finished. Report: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
