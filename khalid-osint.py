import os, subprocess, sys, requests, re
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def run_tool(cmd, name, report_file):
    """Deep Filter: Sirf verified data hi dikhayega"""
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Powerful Filter: Jo data screenshot ki tarah 'Found' ho
                if any(x in clean_line.lower() for x in ["http", "found", "[+]", "target:", "name:", "address:", "father:"]):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error", "failed"]):
                        # Professional Telegram-Style Output
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}[Verified] {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.CYAN}╔════════════════════════════════════════════╗")
    print(f"{Fore.RED}║     KHALID OSINT - GITHUB POWERFUL v2.0    ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Username/Phone/Email): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Sabse Powerful Tools ki list jo Github par active hain
    tools = [
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock"),
        (f"maigret {target} --timeout 10", "Maigret (Deep Search)"),
        (f"holehe {target} --only-used", "Holehe (Email-DB)"),
        (f"phoneinfoga scan -n {target}", "Phone-Intelligence"),
        (f"python3 -m blackbird -u {target}", "Blackbird (Fixed)"),
        (f"photon -u {target} --wayback -l 2", "Web-Crawler")
    ]

    print(f"{Fore.BLUE}[*] Triggering 7+ Powerful Tools in Parallel...\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}[➔] Finished. Data saved in: {report_path}")

if __name__ == "__main__":
    main()
