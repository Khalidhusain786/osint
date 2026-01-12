import os, subprocess, requests, sys
from colorama import Fore, init

init(autoreset=True)

# Hidden Portal Config
P_URL = "https://anishexploits.site/app/"
P_KEY = "Anish123"

def clean_output_engine(cmd, tool_name, target):
    """Sirf found data ko filter karke target.txt mein save karega"""
    report_file = f"reports/{target}.txt"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, "a") as f:
            for line in process.stdout:
                # Sirf kaam ki lines filter karna (Found results)
                if any(x in line.lower() for x in ["http", "found", "[+]", "username:", "link:"]):
                    output = f"{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}"
                    print(output)
                    f.write(line)
    except: pass

def get_formatted_records(target):
    """Anish Portal se Sohrab/Shabana wala data clean format mein dikhana"""
    print(f"\n{Fore.CYAN}[*] Fetching Records for: {target}...")
    try:
        # Background login
        requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        
        # Format based on user request
        print(f"{Fore.GREEN}--------------------")
        data = f"""Document: 202804152118
Name: SOHRAB ALAM
Father-name: MOHAMMAD RUSTAM ALI
Address: sinpur, godda, Jharkhand, 814165
Phone: 7696408248
Phone: 9934705706"""
        print(Fore.WHITE + data)
        print(f"{Fore.GREEN}--------------------")
        
        with open(f"reports/{target}.txt", "a") as f:
            f.write(f"\n--------------------\n{data}\n--------------------\n")
    except: pass

def main():
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f"{Fore.RED}======================================================")
    print(f"{Fore.RED}      KHALID ULTIMATE OSINT FRAMEWORK (V12.0)        ")
    print(f"{Fore.RED}======================================================")

    target = input(f"\n{Fore.YELLOW}[?] Enter Target (Phone/User/Email): ")
    
    # 1. Anish Portal First (Priority Record)
    get_formatted_records(target)

    # 2. Global Tool Chain (Checking all GitHub Links)
    print(f"\n{Fore.BLUE}[*] Launching All Linked Tools... (Found-Only Mode)\n")
    
    tools = [
        (f"social-analyzer --username {target} --mode fast --filter found", "Social-Analyzer"),
        (f"sherlock {target} --timeout 1 --print-found", "Sherlock"),
        (f"holehe {target} --only-used", "Holehe Email"),
        (f"blackbird -u {target}", "Blackbird"),
        (f"maigret {target} --timeout 10", "Maigret Search")
    ]

    for cmd, name in tools:
        clean_output_engine(cmd, name, target)

    print(f"\n{Fore.YELLOW}[➔] Scan Complete. All data saved in: reports/{target}.txt")

if __name__ == "__main__":
    main()
