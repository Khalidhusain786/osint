import os, subprocess, sys
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def run_tool(cmd, name, report_file):
    """Parallel execution with strict output filtering"""
    try:
        # stderr ko devnull bheja hai taaki errors screen par na dikhein
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Sirf 'found' ya 'links' waali lines dikhayega
                if any(x in clean_line.lower() for x in ["http", "found", "[+]", "target", "link:"]):
                    output = f"{Fore.GREEN}[FOUND] {Fore.CYAN}{name}: {Fore.WHITE}{clean_line}"
                    print(output)
                    f.write(f"{name}: {clean_line}\n")
        process.wait()
    except:
        pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.RED}KHALID OSINT - SPEED MODE (FOUND ONLY)")
    target = input(f"\n{Fore.YELLOW}[?] Enter Target: ")
    if not target: return

    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # Ordered list as per your requirement
    tools = [
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock"),
        (f"maigret {target} --timeout 8", "Maigret"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"photon -u {target} --wayback", "Photon"),
        (f"phoneinfoga scan -n {target}", "PhoneInfo")
    ]

    print(f"{Fore.BLUE}[*] Parallel Scan Started... Results will appear as they are found.\n")

    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n{Fore.YELLOW}[➔] All Scans Finished. Clean Report: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
