import os, subprocess, sys
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def run_legacy_tool(cmd, name, report_file):
    """Real-time output scanning with Error Handling"""
    try:
        # subprocess.PIPE se output read karna
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Output ko line by line process karna
        for line in process.stdout:
            clean_line = line.strip()
            # Sirf kaam ki info filter karna
            if any(x in clean_line.lower() for x in ["http", "found", "[+]", "link:", "target:"]):
                output = f"{Fore.CYAN}[+] {name}: {Fore.WHITE}{clean_line}"
                print(output)
                
                # File mein save karna
                with open(report_file, "a") as f:
                    f.write(f"{name}: {clean_line}\n")
        
        process.wait()
    except Exception as e:
        print(f"{Fore.RED}[!] Error in {name}: {e}")

def main():
    if not os.path.exists('reports'): 
        os.makedirs('reports')
    
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Fore.RED}KHALID OSINT - FULL RECOVERY MODE (MULTI-THREADED)")
    
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Username/Phone): ")
    if not target:
        print(f"{Fore.RED}Target cannot be empty!")
        return

    report_path = os.path.abspath(f"reports/{target}.txt")
    
    # Tool commands list
    tools = [
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"sherlock {target} --timeout 5 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe"),
        (f"maigret {target} --timeout 10", "Maigret"),
        (f"social-analyzer --username {target} --mode fast", "SocialAnalyzer"),
        (f"blackbird -u {target}", "Blackbird")
    ]
    
    threads = []
    print(f"{Fore.BLUE}[*] Starting all modules simultaneously...\n")

    # Multi-threading start
    for cmd, name in tools:
        t = Thread(target=run_legacy_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()
        
    print(f"\n{Fore.YELLOW}[➔] All Scans Finished. Report: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
