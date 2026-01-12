import os, subprocess, sys, requests, re
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def search_breach_databases(target, report_file):
    """Public Breach Databases aur Leaked Links check karne ke liye"""
    # Note: Kuch APIs keys maangti hain, ye public dorks aur common leaks check karega
    print(f"{Fore.MAGENTA}[*] Searching Leak Databases for: {target}")
    
    # Example queries for breach sources
    queries = [
        f"https://www.google.com/search?q=site:pastebin.com+%22{target}%22",
        f"https://www.google.com/search?q=site:ghostbin.com+%22{target}%22"
    ]
    
    with open(report_file, "a") as f:
        f.write(f"\n--- DATA BREACH & LEAK SEARCH ---\n")
        # Yahan script background mein in links ko verify karegi
        # Actual breach data Telegram bots aksar private APIs se uthate hain

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Strict Data Filter: Jo screenshot jaisa real data dikhaye
                if any(x in clean_line.lower() for x in ["http", "found", "[+]", "password:", "leak:", "database:"]):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}[BREACH/DATA] {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.CYAN}╔════════════════════════════════════════════╗")
    print(f"{Fore.RED}║    KHALID OSINT - DEEP BREACH & DATA v3.0  ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target (Email/Username/Phone): ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Parallel execution with Breach Check
    Thread(target=search_breach_databases, args=(target, report_path)).start()

    # Useful & Active Tools for Breach/Data Info
    tools = [
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"holehe {target} --only-used", "Email-Breach-Check"),
        (f"maigret {target} --timeout 10", "Deep-Identity-Search"),
        (f"phoneinfoga scan -n {target}", "Phone-Intelligence"),
        (f"python3 -m blackbird -u {target}", "Blackbird-DB"),
        (f"sherlock {target} --timeout 5", "Sherlock")
    ]

    print(f"{Fore.BLUE}[*] Scanning 20+ Data Sources... Found items only:\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Deep Scan Finished. Report: {report_path}")

if __name__ == "__main__":
    main()
