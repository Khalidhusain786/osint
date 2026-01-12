import os, subprocess, requests, time
from colorama import Fore, init

init(autoreset=True)

def check_tor():
    try:
        r = requests.get('https://check.torproject.org', proxies={'http':'socks5://127.0.0.1:9050', 'https':'socks5://127.0.0.1:9050'}, timeout=5)
        return "Congratulations" in r.text
    except: return False

def run_layer(cmd, name, target, color):
    print(f"{color}[*] Scanning {name} Layer...")
    # Background execution with silent error handling
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = res.stdout + res.stderr
    
    # Logic: Agar kuch kaam ka mila toh hi dikhao
    findings = [l.strip() for l in out.split('\n') if any(k in l.lower() for k in ["found", "http", "database", "leaked", "+", "user"])]
    
    if findings:
        print(f"{Fore.GREEN}[✔] SUCCESS: {name} found data!")
        with open(f"reports/{target}_full_report.txt", "a") as f:
            f.write(f"\n--- {name} Results ---\n")
            for line in findings:
                if "404" not in line:
                    print(f"{Fore.WHITE}  ➤ {line}")
                    f.write(line + "\n")
    else:
        # Screen par kuch nahi dikhega agar data nahi mila
        pass

def master_scan():
    os.system('clear')
    print(f"{Fore.RED}KHALID ULTIMATE OSINT: SURFACE | DEEP | DARK | GOV")
    print("-" * 50)
    
    tor = check_tor()
    proxy = "proxychains4 " if tor else ""
    target = input(f"{Fore.YELLOW}[+] Enter Target: ")
    
    # --- LAYER 1: SURFACE WEB (Google/Dorks) ---
    # Har govt domain par check karega target ke liye
    run_layer(f"googler --nocolor -n 5 -w gov.in \"{target}\"", "Gov-India Mirrors", target, Fore.CYAN)
    run_layer(f"googler --nocolor -n 5 \"{target}\" leaked database", "Surface Web Leaks", target, Fore.CYAN)

    # --- LAYER 2: DEEP WEB (Social & Account Footprints) ---
    run_layer(f"{proxy}maigret {target} --brief", "Deep-Social", target, Fore.MAGENTA)
    run_layer(f"holehe {target} --only-used", "Email-Breach", target, Fore.MAGENTA)
    run_layer(f"social-analyzer --username {target} --mode fast", "Social-Analyzer", target, Fore.MAGENTA)

    # --- LAYER 3: DARK WEB (Tor Search Engines) ---
    if tor:
        # Ahmia (Darkweb search engine) ko query karna via proxy
        run_layer(f"proxychains4 curl -s \"https://ahmia.fi/search/?q={target}\" | grep -o 'http[s]*://[^\" ]*'", "Dark-Web Index", target, Fore.RED)

    # --- LAYER 4: TELEGRAM BOT MIRRORS (Optional Python Function) ---
    # Yahan aap apna Telegram wala code call kar sakte hain

    print(f"\n{Fore.GREEN}[!] Scan Complete. Full Path: reports/{target}_full_report.txt")

if __name__ == "__main__":
    master_scan()
