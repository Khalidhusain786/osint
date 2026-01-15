#!/usr/bin/env python3
"""
KHALID HUSAIN786 OSINT v2 - VISUAL ADDON MODULE (COMPLETE VERSION)
✅ 100% COMPATIBLE - NO EXISTING CODE CHANGES REQUIRED
✅ ALL LINKS CLICKABLE + SAVED IN TARGET FOLDER
✅ SINGLE MASTER FOLDER PER TARGET
✅ PLAIN TEXT + RICH VISUALS
✅ COPY-PASTE READY
✅ ALL MISSING FEATURES ADDED
✅ AUTO-DETECTION + ERROR HANDLING
"""

import os
import sys
import re
import webbrowser
import pyperclip
import urllib.parse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json
import subprocess
import shutil
from typing import List, Dict, Any

# RICH VISUALS (FALLBACK TO PLAIN TEXT)
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    from rich.progress import track
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    print("Plain text mode - install 'rich' for visuals: pip install rich")
    class FakeConsole:
        def print(self, *args, **kwargs): print(*args, **kwargs)
    console = FakeConsole()

# COLORS (FALLBACK)
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    class FakeColors:
        RED = Back.RED = Style.RESET_ALL = YELLOW = GREEN = CYAN = MAGENTA = WHITE = RESET = ""
    Fore = Back = Style = FakeColors()

class KhalidVisualAddon:
    def __init__(self, target="UNKNOWN"):
        self.target = self._sanitize_target(target)
        self.master_folder = Path(f"./KHALID_MASTER_{self.target}")
        self.master_folder.mkdir(exist_ok=True)
        
        # ALL LINKS STORAGE
        self.all_links = defaultdict(list)
        self.hit_count = 0
        
        # FILES
        self.links_file = self.master_folder / f"{self.target}_ALL_LINKS.txt"
        self.summary_file = self.master_folder / f"{self.target}_SUMMARY.json"
        self.clicks_file = self.master_folder / f"{self.target}_CLICKS.txt"
        self.stats_file = self.master_folder / f"{self.target}_STATS.txt"
        
        # Load existing data
        self._load_existing_data()
    
    def _sanitize_target(self, target: str) -> str:
        """Sanitize target name for folder/filenames"""
        return re.sub(r'[^\w\-_.]', '_', str(target).replace("@", "_").replace("+", "x"))[:50]
    
    def _load_existing_data(self):
        """Load existing links/stats on startup"""
        if self.links_file.exists():
            try:
                with open(self.links_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.hit_count = len(re.findall(r'\[\d+\]', content))
                
                # Load JSON summary if exists
                if self.summary_file.exists():
                    with open(self.summary_file, 'r') as f:
                        summary = json.load(f)
                        self.all_links.update({k: v for k, v in summary.get('by_type', {}).items()})
            except:
                pass
    
    def detect_links(self, text: str) -> List[str]:
        """Enhanced link detection with multiple patterns"""
        patterns = [
            r'https?://[^\s<>"\']+(?:[^\s<>"\'\.<>]|/)*',
            r'www\.[^\s<>"\']+(?:[^\s<>"\'\.<>]|/)*',
            r'(?:bit\.ly|t\.co|tinyurl\.com)/[^\s<>"\']*',
            r'http[^\s]*',  # Fallback
            r'ftp://[^\s<>"\']*'
        ]
        links = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            links.extend(found)
        
        # Clean and dedupe
        cleaned_links = []
        for link in links:
            link = link.strip('.,;?!').rstrip('/')
            if len(link) > 10 and link not in cleaned_links:
                cleaned_links.append(link)
        
        return cleaned_links
    
    def save_link(self, link: str, hit_type: str = "UNKNOWN", source: str = ""):
        """Save link with full metadata"""
        if not link.startswith(('http', 'www', 'ftp')):
            link = 'https://' + link
            
        link_data = {
            'url': link,
            'type': hit_type,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'id': self.hit_count
        }
        
        self.all_links[hit_type].append(link_data)
        
        # APPEND TO TEXT FILE (CLICKABLE + COLORED)
        color_map = {
            'EMAIL': Fore.CYAN, 'PHONE': Fore.GREEN, 'SOCIAL': Fore.MAGENTA,
            'CARD': Fore.RED, 'DARKWEB': Fore.YELLOW, 'PROFILE': Fore.BLUE
        }
        color = color_map.get(hit_type, Fore.WHITE)
        
        with open(self.links_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{self.hit_count:03d}] {color}{link}{Fore.RESET}\n")
            f.write(f"   Type: {hit_type:<12} | Source: {source:<15} | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"   📋 Copy: {link}\n")
            f.write(f"   🌐 Click: python3 {sys.argv[0]} OPEN {self.hit_count}\n")
            f.write("-" * 80 + "\n")
        
        self.hit_count += 1
    
    def display_clickable_links(self, limit: int = 0):
        """Enhanced dashboard with statistics"""
        total_links = self.hit_count
        type_counts = {k: len(v) for k, v in self.all_links.items()}
        
        if RICH_AVAILABLE:
            # STATS PANEL
            stats_table = Table(title=f"📊 {self.target} - {total_links} LINKS", box=box.ROUNDED)
            stats_table.add_column("TYPE", style="bold magenta")
            stats_table.add_column("COUNT", justify="right", style="bold cyan")
            stats_table.add_column("LATEST", style="green")
            
            for hit_type in sorted(type_counts, key=type_counts.get, reverse=True):
                count = type_counts[hit_type]
                latest = self.all_links[hit_type][-1]['url'][:40] + "..." if count else "-"
                stats_table.add_row(hit_type, str(count), latest)
            
            console.print(stats_table)
            
            # LINKS TABLE (show top 10 or all if limit=0)
            show_limit = min(10, total_links) if limit == 0 else min(limit, total_links)
            links_table = Table(title=f"🔗 TOP {show_limit} LINKS", box=box.ROUNDED)
            links_table.add_column("ID", style="cyan", no_wrap=True)
            links_table.add_column("TYPE", style="magenta")
            links_table.add_column("LINK", style="green")
            links_table.add_column("SOURCE", style="yellow")
            links_table.add_column("CLICK", justify="right")
            
            all_links_flat = []
            for hit_type, links_list in self.all_links.items():
                all_links_flat.extend(links_list)
            
            for link_data in sorted(all_links_flat, key=lambda x: x['id'], reverse=True)[:show_limit]:
                cmd = f"python3 {sys.argv[0]} OPEN {link_data['id']}"
                short_url = (link_data['url'][:60] + "...") if len(link_data['url']) > 60 else link_data['url']
                links_table.add_row(
                    f"[{link_data['id']:03d}]",
                    link_data['type'],
                    short_url,
                    link_data['source'][:12],
                    cmd
                )
            
            console.print(links_table)
            
            # SUMMARY PANEL
            console.print(Panel.fit(
                f"[bold cyan]📁 Folder:[/bold cyan] {self.master_folder}\n"
                f"[bold green]💾 Files:[/bold green] Links({total_links}), Summary, Clicks\n"
                f"[bold yellow]⚡ Commands:[/bold yellow] LIST | OPEN 123 | COPY | STATS | CLEAN",
                title="🚀 DASHBOARD", border_style="bright_blue"
            ))
        else:
            print(f"\n🎯 TARGET: {self.target} | TOTAL: {total_links} links")
            print(f"📁 FOLDER: {self.master_folder}")
            print("\n📊 STATS:")
            for hit_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {hit_type:<12}: {count}")
            print("\n🔗 TOP LINKS:")
            all_links_flat = []
            for links_list in self.all_links.values():
                all_links_flat.extend(links_list)
            for link_data in sorted(all_links_flat, key=lambda x: x['id'], reverse=True)[:5]:
                print(f"  [{link_data['id']:03d}] {link_data['type']:<10} {link_data['url'][:60]}...")
    
    def open_link(self, link_id: int) -> bool:
        """Open specific link in browser"""
        for hit_type, links in self.all_links.items():
            for link_data in links:
                if link_data['id'] == link_id:
                    url = link_data['url']
                    print(f"🌐 OPENING [{link_id:03d}]: {url}")
                    
                    # LOG CLICK
                    with open(self.clicks_file, 'a', encoding='utf-8') as f:
                        f.write(f"{datetime.now()}: Opened {link_id} -> {url}\n")
                    
                    # OPEN IN BROWSER
                    webbrowser.open(url)
                    
                    # COPY TO CLIPBOARD
                    pyperclip.copy(url)
                    print(f"📋 URL COPIED TO CLIPBOARD!")
                    return True
        
        print(f"❌ Link ID {link_id} not found!")
        return False
    
    def copy_all_links(self):
        """Copy all links categorized to clipboard"""
        links_text = f"KHALID OSINT - {self.target}\n"
        links_text += f"Total Links: {self.hit_count} | Folder: {self.master_folder}\n\n"
        
        for hit_type, links in sorted(self.all_links.items(), key=lambda x: len(x[1]), reverse=True):
            links_text += f"\n{'='*60}\n"
            links_text += f"{hit_type.upper()} ({len(links)})\n"
            links_text += f"{'='*60}\n"
            for link in links[:10]:  # Top 10 per category
                links_text += f"🔗 {link['url']}\n"
                links_text += f"   {link['source']} | {link['timestamp'][:19]}\n"
        
        pyperclip.copy(links_text)
        print(f"📋 COPIED {self.hit_count} LINKS TO CLIPBOARD!")
    
    def save_summary(self):
        """Save complete JSON summary"""
        summary = {
            'target': self.target,
            'total_links': self.hit_count,
            'timestamp': datetime.now().isoformat(),
            'folder': str(self.master_folder),
            'by_type': {k: [link['url'] for link in v] for k, v in self.all_links.items()}
        }
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    def show_stats(self):
        """Detailed statistics"""
        if not self.links_file.exists():
            print("No data yet!")
            return
        
        stats = {
            'total_links': self.hit_count,
            'unique_domains': len(set(re.findall(r'://([^/]+)', open(self.links_file).read()))),
            'top_sources': defaultdict(int)
        }
        
        content = open(self.links_file).read()
        for line in content.split('\n'):
            if 'Source:' in line:
                source = line.split('Source: ')[1].split('|')[0].strip()
                stats['top_sources'][source] += 1
        
        if RICH_AVAILABLE:
            stats_table = Table(title="📈 DETAILED STATS", box=box.ROUNDED)
            stats_table.add_column("METRIC", style="bold cyan")
            stats_table.add_column("VALUE", style="bold green")
            stats_table.add_row("Total Links", str(stats['total_links']))
            stats_table.add_row("Unique Domains", str(stats['unique_domains']))
            stats_table.add_row("Files Created", str(len(list(self.master_folder.glob('*')))))
            console.print(stats_table)
            
            sources_table = Table(title="🔍 TOP SOURCES", box=box.ROUNDED)
            sources_table.add_column("SOURCE", style="yellow")
            sources_table.add_column("HITS", justify="right")
            for source, count in sorted(stats['top_sources'].items(), key=lambda x: x[1], reverse=True)[:10]:
                sources_table.add_row(source, str(count))
            console.print(sources_table)
        else:
            print(f"📊 STATS: {stats['total_links']} links, {stats['unique_domains']} domains")
    
    def clean_target(self):
        """Clean all data for this target"""
        if self.master_folder.exists():
            shutil.rmtree(self.master_folder)
            print(f"🧹 CLEANED: {self.master_folder}")
        else:
            print("No data to clean!")
    
    def export_html(self):
        """Export clickable HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html><head><title>KHALID OSINT - {self.target}</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            .link {{ color: #0066cc; text-decoration: none; font-family: monospace; }}
            .link:hover {{ background: #e6f3ff; }}
            .type {{ color: #666; font-weight: bold; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background: #f2f2f2; }}
        </style></head><body>
        <h1>🔍 KHALID OSINT REPORT - {self.target}</h1>
        <p>Total: {self.hit_count} links | <a href="file://{self.master_folder}">📁 Folder</a></p>
        <table>
        <tr><th>ID</th><th>Type</th><th>Link</th><th>Source</th><th>Date</th></tr>
        """
        
        all_links_flat = []
        for hit_type, links_list in self.all_links.items():
            all_links_flat.extend(links_list)
        
        for link_data in sorted(all_links_flat, key=lambda x: x['id'], reverse=True):
            short_url = link_data['url'][:80] + "..." if len(link_data['url']) > 80 else link_data['url']
            html_content += f"""
            <tr>
                <td><b>{link_data['id']}</b></td>
                <td class="type">{link_data['type']}</td>
                <td><a class="link" href="{link_data['url']}" target="_blank">{short_url}</a></td>
                <td>{link_data['source']}</td>
                <td>{link_data['timestamp'][:19]}</td>
            </tr>
            """
        
        html_content += "</table></body></html>"
        
        html_file = self.master_folder / f"{self.target}_REPORT.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 HTML REPORT: {html_file}")
        webbrowser.open(f"file://{html_file}")

def main():
    if len(sys.argv) < 2:
        print("🚀 KHALID HUSAIN786 OSINT Visual Addon v2")
        print("Usage:")
        print("  python3 KhalidVisual.py john@gmail.com          # New target")
        print("  python3 KhalidVisual.py john@gmail.com LIST      # Show dashboard")
        print("  python3 KhalidVisual.py john@gmail.com OPEN 123  # Open link ID")
        print("  python3 KhalidVisual.py john@gmail.com COPY      # Copy all links")
        print("  python3 KhalidVisual.py john@gmail.com STATS     # Show stats")
        print("  python3 KhalidVisual.py john@gmail.com HTML      # Export HTML")
        print("  python3 KhalidVisual.py john@gmail.com CLEAN     # Delete all data")
        return
    
    target = sys.argv[1]
    addon = KhalidVisualAddon(target)
    
    # COMMANDS
    if len(sys.argv) > 2:
        cmd = sys.argv[2].upper()
        
        if cmd == "OPEN" and len(sys.argv) > 3:
            addon.open_link(int(sys.argv[3]))
            return
        
        elif cmd == "LIST":
            addon.display_clickable_links()
            return
        
        elif cmd == "COPY":
            addon.copy_all_links()
            return
        
        elif cmd == "STATS":
            addon.show_stats()
            return
        
        elif cmd == "HTML":
            addon.export_html()
            return
        
        elif cmd == "CLEAN":
            addon.clean_target()
            return
    
    # DEFAULT MODE - SHOW DASHBOARD + EXAMPLE
    print(f"🎯 TARGET LOADED: {addon.target}")
    addon.display_clickable_links()
    addon.save_summary()
    
    # EXAMPLE INTEGRATION
    print("\n💡 INTEGRATION EXAMPLE:")
    print("addon = KhalidVisualAddon('target@example.com')")
    print("addon.save_link('https://example.com/leak', 'EMAIL', 'haveibeenpwned')")
    print("addon.display_clickable_links()")

# EASY INTEGRATION FOR YOUR MAIN SCRIPT
"""
# === ADD THESE 3 LINES TO ANY SCRIPT ===
from KhalidVisual import KhalidVisualAddon
addon = KhalidVisualAddon("your_target")
addon.save_link(found_url, hit_type="EMAIL", source="tool_name")
addon.display_clickable_links()
"""

if __name__ == "__main__":
    main()
