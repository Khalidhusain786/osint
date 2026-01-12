import os, subprocess, sys, requests, re
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def check_anish_exploits(target):
    """Automatic login and search for AnishExploits"""
    # Note: Login logic adjusted for automated session
    url = "https://anishexploits.site/app/"
    try:
        # Simple fetch to see if data is public or needs specific POST
        res = requests.get(f"{url}?search={target}", timeout=5)
        if "found" in res.text.lower():
            print(f"{Fore.GREEN}[DATABASE] AnishExploits: Match found for {target}!")
    except: pass

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # TELEGRAM BOT FILTER: Sirf kaam ka data dikhao
                triggers = ["http", "found", "[+]", "name:", "address:", "father", "phone:"]
                if any(x in clean_line.lower() for x in triggers):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error"]):
                        # Formatting like the screenshot
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}➤ {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.CYAN}╔════════════════════════════════════════════╗")
    print(f"{Fore.RED}║        KHALID OSINT - DATABASE SEARCH      ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Username/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Start AnishExploits Check
    Thread(target=check_anish_exploits, args=(target,)).start()

    # Organized Tool List (Fastest First)
    tools = [
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"holehe {target} --only-used", "Email-Check"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"phoneinfoga scan -n {target}", "Phone-Lookup")
    ]

    print(f"{Fore.BLUE}[*] Searching multiple databases... Please wait.\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}[!] Finished. Report Saved: {report_path}")

if __name__ == "__main__":
    main()
