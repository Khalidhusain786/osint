import os, subprocess, sys, re
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def clean_output(line):
    """Faltu symbols aur extra spaces hatane ke liye"""
    return re.sub(r'\s+', ' ', line).strip()

def run_tool(cmd, name, report_file):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = clean_output(line)
                
                # SIRF VALID DATA FILTER: Jo link ho ya jisme specific keywords hon
                valid_triggers = ["http", "found", "user:", "name:", "address:", "phone:", "location:"]
                bad_keywords = ["not found", "404", "error", "failed", "no results", "checking"]

                if any(x in clean_line.lower() for x in valid_triggers):
                    if not any(bad in clean_line.lower() for bad in bad_keywords):
                        # Telegram Style Formatting
                        display_text = f"{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━\n{Fore.YELLOW}[+] {name}: {Fore.WHITE}{clean_line}"
                        print(display_text)
                        f.write(f"{name}: {clean_line}\n")
        process.wait()
    except:
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.RED}      KHALID OSINT - VERIFIED DATA ENGINE")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    target = input(f"\n{Fore.WHITE}❯ Enter Target (Username/Phone): ")
    if not target: return

    report_path = os.path.abspath(f"reports/{target}.txt")
    print(f"\n{Fore.BLUE}[*] Searching databases for: {target}...\n")

    # Sabhi tools list (Jo screenshots mein missing the unhe fix kiya hai)
    tools = [
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock"),
        (f"maigret {target} --timeout 8", "Maigret"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"phoneinfoga scan -n {target}", "PhoneInfo")
    ]

    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n{Fore.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.YELLOW}[➔] Scan Finished. Data saved in: {report_path}")

if __name__ == "__main__":
    main()
