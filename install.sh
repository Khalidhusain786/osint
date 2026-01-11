cd ~/osint
# Update the search script to show ALL raw data found
cat <<EOF > khalid-osint.py
import os, subprocess
from colorama import Fore, init
init(autoreset=True)

def bot():
    print(Fore.RED + "--- KHALID GLOBAL SEARCH (FINAL FIXED) ---")
    target = input(Fore.WHITE + "[+] Target (Name/Phone/Email): ")
    print(Fore.YELLOW + "[*] Scanning Hidden & Deep Layers...")
    
    # Using Maigret with increased verbosity to ensure output is captured
    res = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
    
    print(Fore.GREEN + "\n🔔 DATA RESULTS:")
    print(Fore.WHITE + "═"*55)
    
    output = res.stdout.strip()
    if output:
        # Har line ko format ke sath print karna
        for line in output.split('\n'):
            print(f"{Fore.CYAN}➤ {line}")
    else:
        # Fallback agar tool ko format samajh na aaye
        print(Fore.RED + "➤ Status: Search complete. Please check the reports folder if empty.")
    
    print(Fore.WHITE + "═"*55)
    os.makedirs(f"reports/{target}", exist_ok=True)
    with open(f"reports/{target}/report.txt", "w") as f:
        f.write(output if output else "No data found.")

if __name__ == "__main__":
    bot()
EOF

# Correct Desktop Shortcut for Kali Root
cat <<EOF > /root/Desktop/Khalid-OSINT.desktop
[Desktop Entry]
Name=Khalid OSINT
Exec=qterminal -e "bash -c 'cd /root/osint && python3 khalid-osint.py; exec bash'"
Icon=security-high
Terminal=true
Type=Application
EOF
chmod +x /root/Desktop/Khalid-OSINT.desktop
