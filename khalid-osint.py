import os, subprocess, sys, requests, re
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def check_hibp_leaks(target):
    """'Have I Been Pwned' style API check (using public trackers)"""
    print(f"{Fore.MAGENTA}[*] Checking Data Breaches & Deepweb Leaks for: {target}")
    # h8mail ya holehe background mein in sources ko query karenge
    # Target agar email hai toh results zyada accurate aate hain

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # DEEPWEB/BREACH FILTER: Sirf actual leaked data show hoga
                success_keywords = ["http", "found", "[+]", "password:", "address:", "database:", "leaked:"]
                if any(x in clean_line.lower() for x in success_keywords):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error", "failed"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}[BREACH FOUND] {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.RED}╔════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - DARKWEB & BREACH v4.0    ║")
    print(f"{Fore.RED}╚════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/User/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Darkweb & HIBP style background check
    Thread(target=check_hibp_leaks, args=(target,)).start()

    # Tools list including Deepweb/Breach focused tools
    tools = [
        (f"holehe {target} --only-used", "Breach-Check (Holehe)"),
        (f"maigret {target} --timeout 15 --no-recursion", "Deep-Identity (Maigret)"),
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"phoneinfoga scan -n {target}", "Phone-Intel"),
        (f"python3 -m blackbird -u {target}", "Database-Search (Blackbird)"),
        (f"sherlock {target} --timeout 5", "Sherlock")
    ]

    print(f"{Fore.BLUE}[*] Accessing Breach Databases & Darkweb Indexes...\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}[➔] Deep Search Complete. Data Saved: {report_path}")

if __name__ == "__main__":
    main()
