import os, subprocess, sys, requests, re
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

# Tor Proxy Setup (Agar Tor Browser ya Service on hai)
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def search_darkweb_engines(target, report_file):
    """Ahmia aur Onion indexes se data nikalne ke liye"""
    print(f"{Fore.MAGENTA}[*] Deep Searching Darkweb (Onion Indexes) for: {target}")
    
    # Ahmia Search (Clear-web gateway to Onion)
    ahmia_url = f"https://ahmia.fi/search/?q={target}"
    try:
        res = requests.get(ahmia_url, timeout=10)
        onions = re.findall(r'[a-z2-7]{16,56}\.onion', res.text)
        
        if onions:
            with open(report_file, "a") as f:
                f.write(f"\n--- DARK WEB LEAKS ---\n")
                for link in list(set(onions)):
                    output = f"{Fore.GREEN}[ONION LINK] Found: {Fore.WHITE}http://{link}"
                    print(output)
                    f.write(f"{link}\n")
    except: pass

def run_tool(cmd, name, report_file):
    try:
        # Standard output aur errors handle karna
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Strict Data Triggers
                if any(x in clean_line.lower() for x in ["http", "found", "[+]", "password:", "address:", "father", "leaked:"]):
                    if not any(bad in clean_line.lower() for bad in ["not found", "404", "error", "searching"]):
                        print(f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━")
                        print(f"{Fore.YELLOW}[+] {name}: {Fore.WHITE}{clean_line}")
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════╗")
    print(f"{Fore.RED}║   KHALID OSINT v5.0 - DEEP & DARKWEB MONSTER     ║")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝")
    
    target = input(f"\n{Fore.WHITE}❯❯ Enter Target ID/Email/Phone: ")
    if not target: return
    report_path = os.path.abspath(f"reports/{target}.txt")

    # Darkweb Search background mein trigger
    Thread(target=search_darkweb_engines, args=(target, report_path)).start()

    # Sabse powerful GitHub aur CLI tools ka combination
    tools = [
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"h8mail -t {target} -q", "Breach-Hunter (HIBP)"),
        (f"holehe {target} --only-used", "Email-Lookup"),
        (f"maigret {target} --timeout 15 --no-recursion", "Deep-ID (Maigret)"),
        (f"phoneinfoga scan -n {target}", "Phone-Intelligence"),
        (f"python3 -m blackbird -u {target}", "Blackbird-DB"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock")
    ]

    print(f"{Fore.BLUE}[*] Accessing Darkweb Nodes & Global Databases...\n")
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Investigation Finished. Results: {report_path}")

if __name__ == "__main__":
    main()
