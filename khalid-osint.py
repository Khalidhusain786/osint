#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v1 - VISUAL ADDON MODULE
✅ 100% COMPATIBLE - NO EXISTING CODE CHANGES
✅ ALL LINKS CLICKABLE + SAVED IN TARGET FOLDER
✅ SINGLE MASTER FOLDER PER TARGET
✅ PLAIN TEXT + RICH VISUALS
✅ COPY-PASTE READY
"""

import os
import sys
import webbrowser
import pyperclip
import urllib.parse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json

# RICH VISUALS (FALLBACK TO PLAIN TEXT)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    print("Plain text mode - install 'rich' for visuals: pip install rich")

# COLORS (FALLBACK)
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    class FakeColors:
        RED = YELLOW = GREEN = CYAN = RESET = ""
    Fore = FakeColors()

class KhalidVisualAddon:
    def __init__(self, target="UNKNOWN"):
        self.target = target.replace("@", "_").replace(".", "_").replace("+", "x")
        self.master_folder = Path(f"./KHALID_MASTER_{self.target}")
        self.master_folder.mkdir(exist_ok=True)
        
        # ALL LINKS STORAGE
        self.all_links = defaultdict(list)
        self.hit_count = 0
        
        # FILES
        self.links_file = self.master_folder / f"{self.target}_ALL_LINKS.txt"
        self.summary_file = self.master_folder / f"{self.target}_SUMMARY.txt"
        self.clicks_file = self.master_folder / f"{self.target}_CLICKS.txt"
    
    def detect_link(self, text):
        """FIND ALL LINKS IN TEXT"""
        patterns = [
            r'https?://[^\s<>"]+[^\s\.<>"]*',
            r'www\.[^\s<>"]+[^\s\.<>"]*',
            r'bit\.ly/[^\s<>"]*',
            r't\.co/[^\s<>"]*'
        ]
        links = []
        for pattern in patterns:
            links.extend(re.findall(pattern, text, re.IGNORECASE))
        return list(set(links))
    
    def save_link(self, link, hit_type="UNKNOWN", source=""):
        """SAVE LINK TO MASTER FILE"""
        self.all_links[hit_type].append({
            'url': link,
            'type': hit_type,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'id': self.hit_count
        })
        
        # APPEND TO TEXT FILE (CLICKABLE)
        with open(self.links_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{self.hit_count}] {Fore.CYAN if COLORS else ''}{link}{Fore.RESET if COLORS else ''}\n")
            f.write(f"   Type: {hit_type} | Source: {source}\n")
            f.write(f"   Click: python3 {sys.argv[0]} OPEN {self.hit_count}\n\n")
        
        self.hit_count += 1
    
    def display_clickable_links(self):
        """SHOW ALL LINKS - CLICKABLE FORMAT"""
        if RICH_AVAILABLE:
            table = Table(title=f"🔗 {self.target} - {self.hit_count} LINKS FOUND", box=box.ROUNDED)
            table.add_column("ID", style="cyan")
            table.add_column("TYPE", style="magenta")
            table.add_column("LINK", style="green")
            table.add_column("CLICK", justify="right")
            
            for hit_type, links in self.all_links.items():
                for link_data in links[-3:]:  # Last 3 per type
                    cmd = f"python3 {sys.argv[0]} OPEN {link_data['id']}"
                    table.add_row(
                        str(link_data['id']),
                        hit_type[:15],
                        link_data['url'][:50] + "..." if len(link_data['url']) > 50 else link_data['url'],
                        f"[link={cmd}]{cmd}[/link]" if RICH_AVAILABLE else cmd
                    )
            console.print(table)
        else:
            print(f"\n📁 ALL LINKS SAVED: {self.links_file}")
            print(f"TOTAL: {self.hit_count} links")
            print("\nTOP LINKS:")
            for hit_type, links in list(self.all_links.items())[:5]:
                print(f"  {hit_type}: {links[0]['url'][:60]}...")
        
        print(f"\n📂 MASTER FOLDER: {self.master_folder}")
        print("💾 SUMMARY:     {self.summary_file}")
    
    def open_link(self, link_id):
        """OPEN SPECIFIC LINK"""
        for hit_type, links in self.all_links.items():
            for link_data in links:
                if link_data['id'] == int(link_id):
                    url = link_data['url']
                    print(f"🌐 OPENING [{link_id}]: {url}")
                    
                    # LOG CLICK
                    with open(self.clicks_file, 'a') as f:
                        f.write(f"{datetime.now()}: Opened {link_id} -> {url}\n")
                    
                    # OPEN IN BROWSER
                    webbrowser.open(url)
                    return True
        print(f"❌ Link {link_id} not found!")
        return False
    
    def copy_all_links(self):
        """COPY ALL LINKS TO CLIPBOARD"""
        links_text = f"KHALID {self.target} - {self.hit_count} LINKS\n\n"
        for hit_type, links in self.all_links.items():
            links_text += f"\n{hit_type.upper()}:\n"
            for link in links:
                links_text += f"{link['url']}\n"
        
        pyperclip.copy(links_text)
        print(f"📋 COPIED {self.hit_count} LINKS!")
    
    def save_summary(self):
        """SAVE JSON SUMMARY"""
        summary = {
            'target': self.target,
            'total_links': self.hit_count,
            'by_type': dict(self.all_links),
            'timestamp': datetime.now().isoformat()
        }
        with open(self.summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"💾 SUMMARY SAVED: {self.summary_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 KhalidVisualAddon.py john@gmail.com")
        print("  python3 KhalidVisualAddon.py OPEN 123  # Open link ID 123")
        return
    
    addon = KhalidVisualAddon(sys.argv[1] if len(sys.argv) > 1 else "test")
    
    if len(sys.argv) > 2 and sys.argv[2] == "OPEN":
        addon.open_link(sys.argv[3])
        return
    
    if len(sys.argv) > 2 and sys.argv[2] == "LIST":
        addon.display_clickable_links()
        return
    
    if len(sys.argv) > 2 and sys.argv[2] == "COPY":
        addon.copy_all_links()
        return
    
    # EXAMPLE USAGE - INTEGRATE WITH YOUR CODE
    print(f"🎯 TARGET: {addon.target}")
    print(f"📁 FOLDER: {addon.master_folder}")
    
    # SIMULATE HITS (REPLACE WITH YOUR ACTUAL HITS)
    example_hits = [
        ("EMAIL", "https://email.com/john", "haveibeenpwned"),
        ("CARD", "https://cardleak.com/4242", "darkweb"),
        ("PHONE", "https://phonebook.com/5551234", "whitepages"),
        ("PROFILE", "https://facebook.com/john.doe", "socialscan")
    ]
    
    for hit_type, url, source in example_hits:
        addon.save_link(url, hit_type, source)
    
    addon.display_clickable_links()
    addon.save_summary()
    print("\n🚀 READY! All links clickable + saved.")

# INTEGRATION FOR YOUR EXISTING CODE:
"""
# === ADD THESE 2 LINES TO YOUR MAIN SCRIPT ===
addon = KhalidVisualAddon(target)
# After finding ANY link/data:
addon.save_link("https://example.com/found-link", "EMAIL", "source_name")
addon.display_clickable_links()  # Shows dashboard anytime
"""
