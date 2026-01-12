import os, subprocess, sys
from colorama import Fore, init
from threading import Thread

init(autoreset=True)

def run_tool(cmd, name, report_file):
    """Har tool ka output screen par dikhayega aur file mein save karega"""
    try:
        # Popen use kiya hai taaki live output dikhe
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        with open(report_file, "a") as f:
            f.write(f"\n--- {name} Results ---\n")
            for line in process.stdout:
                clean_line = line.strip()
                if clean_line:
                    # Screen par dikhane ke liye
                    print(f"{Fore.CYAN}[{name}] {Fore.WHITE}{clean_line}")
                    # File mein save karne ke liye
                    f.write(f"{clean_line}\n")
        process.wait()
    except Exception as e:
        print(f"{Fore.RED}[!] Error running {name}: {e}")

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{Fore.RED}KHALID OSINT - ULTIMATE RECOVERY (30+ TOOLS)")
    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Username/Phone/Email): ")
    
    if not target:
        print(f"{Fore.RED}Invalid Target!")
        return

    # Report path usi name se save hoga
    report_path = os.path.abspath(f"reports/{target}.txt")
    print(f"{Fore.GREEN}[*] Output will be saved to: {report_path}\n")

    # Saare tools ki list jo aapne bataye
    tools = [
        # Username Tools
        (f"sherlock {target} --timeout 5", "Sherlock"),
        (f"maigret {target} --timeout 15", "Maigret"),
        (f"social-analyzer --username {target} --mode fast", "Social-Analyzer"),
        (f"blackbird -u {target}", "Blackbird"),
        # Email & Phone Tools
        (f"holehe {target} --only-used", "Holehe"),
        (f"phoneinfoga scan -n {target}", "PhoneInfo"),
        (f"ghunt email {target}", "GHunt"),
        # Web Recon
        (f"photon -u {target} --wayback", "Photon"),
        (f"finalrecon --full {target}", "FinalRecon")
    ]

    threads = []
    for cmd, name in tools:
        # Parallel execution for speed
        t = Thread(target=run_tool, args=(cmd, name, report_path))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n{Fore.YELLOW}[➔] Scan Complete! Report: {Fore.WHITE}{report_path}")

if __name__ == "__main__":
    main()
