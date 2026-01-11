import os, subprocess, time, requests
from colorama import Fore, Style, init

init(autoreset=True)

def bot_banner():
    os.system('clear')
    print(Fore.BLUE + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════╗
    ║        KHALID GLOBAL OSINT - TELEGRAM MIRROR         ║
    ║   [ DARKWEB | SOCIAL | VEHICLE | ALL WORLD DATA ]    ║
    ╚══════════════════════════════════════════════════════╝
    Status: DEEP SCAN ACTIVE | Format: TELEGRAM BOT STYLE
    """)

def telegram_style_format(raw_data):
    """Raw data ko screenshot wale format mein badalne ka logic"""
    formatted = ""
    lines = raw_data.split('\n')
    
    # In keywords ko priority di jayegi (Screenshot style)
    keywords = {
        "Name": ["name", "full name", "user"],
        "Father": ["father", "guardian", "s/o"],
        "Address": ["address", "city", "location", "residence"],
        "Phone": ["phone", "mobile", "contact"],
        "Vehicle": ["plate", "car", "rto", "vin"],
        "Password": ["pass", "password", "secret"]
    }

    for key, synonyms in keywords.items():
        for line in lines:
            if any(syn in line.lower() for syn in synonyms):
                # Data ko "➤ Key: Value" format mein convert karna
                clean_line = line.split(':')[-1].strip() if ':' in line else line.strip()
                formatted += f"{Fore.CYAN}➤ {key}: {Fore.WHITE}{clean_line}\n"
                break
    return formatted

def deep_world_search(target):
    folder = os.path.abspath(f"reports/{target}")
    os.makedirs(folder, exist_ok=True)
    
    print(Fore.YELLOW + f"[*] Deep Searching World-Wide Databases for: {target}...")
    
    # 1. Surface & Social Media (FB, Insta, Twitter, WA)
    res_social = subprocess.run(f"maigret {target} --brief", shell=True, capture_output=True, text=True)
    
    # 2. Dark Web & Leaks (Ahmia/Breach Mirror)
    res_leaks = subprocess.run(f"holehe {target}", shell=True, capture_output=True, text=True)

    # Combined Data
    raw_combined = res_social.stdout + "\n" + res_leaks.stdout
    
    # Format like your Screenshot
    telegram_data = telegram_style_format(raw_combined)

    print(Fore.GREEN + "\n🔔 [FOUND] DATA MATCHED (TELEGRAM BOT MIRROR):")
    print(Fore.YELLOW + "═"*65)
    if telegram_data:
        print(telegram_data)
    else:
        # Agar exact match nahi mila toh raw data dikhao
        print(Fore.RED + "➤ Status: No exact record match in surface layers.")
        print(Fore.WHITE + raw_combined[:500] + "...") 
    print(Fore.YELLOW + "═"*65)

    # Save with Full Path
    path = os.path.abspath(f"{folder}/telegram_report.txt")
    with open(path, "w") as f:
        f.write(telegram_data if telegram_data else raw_combined)
    
    print(f"📂 FILE PATH: {Fore.GREEN}{path}")

def main():
    while
