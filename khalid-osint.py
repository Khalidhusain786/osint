import os, subprocess, sys
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def run_tool(cmd, name, report_file):
    try:
        # check=False rakha hai taaki tool missing hone par script na ruke
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        found_anything = False
        with open(report_file, "a") as f:
            for line in process.stdout:
                clean_line = line.strip()
                # Sirf tabhi print karein jab tool kuch dhundh le (links ya matches)
                if any(x in clean_line.lower() for x in ["http", "found", "[+]", "target", "user"]):
                    print(f"{Fore.CYAN}[{name}] {Fore.WHITE}{clean_line}")
                    f.write(f"{name}: {clean_line}\n")
                    found_anything = True
        
        process.wait()
        if not found_anything:
            # Agar tool ne kuch nahi dhundha toh info ke liye
            pass 
    except Exception:
        pass # Quietly skip if tool fails

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    
    print(f"{Fore.RED}KHALID OSINT - STABLE RECOVERY MODE")
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Username/Phone): ")
    if not target: return

    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # In commands ko update kiya hai taaki crash na ho
    tools = [
        (f"sherlock {target} --timeout 5", "Sherlock"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"photon -u {target}", "Photon")
    ]

    print(f"{Fore.BLUE}[*] Scanning started... Found results will appear below:\n")
    
    threads = []
    for cmd, name in tools:
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n{Fore.YELLOW}[➔] Finished. Check Report: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
