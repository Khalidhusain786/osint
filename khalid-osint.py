def extract_pii(self, text):
    pii_data = {}
    text_lower = text.lower()
    
    patterns = self.pii_patterns()
    all_matches = {}
    
    # Extract ALL matches first
    for pii_type, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        if matches:
            all_matches[pii_type] = matches
    
    # Process each type with proper display
    for pii_type, matches in all_matches.items():
        value = matches[0]
        
        if 'PASSWORD' in pii_type:
            raw_pass = value
            masked_pass = '*' * (len(raw_pass)-4) + raw_pass[-4:] if len(raw_pass) > 4 else '*' * len(raw_pass)
            pii_data['🔐 RAW PASS'] = raw_pass[:50]
            pii_data['🔒 MASKED'] = masked_pass
        elif 'PASSWORD_HASH' in pii_type:
            pii_data['🔑 HASH'] = value[:32] + '...' if len(value) > 32 else value
        elif 'PHONE' in pii_type:
            pii_data[f'📞 {pii_type}'] = value
        elif 'VEHICLE' in pii_type:
            pii_data[f'🚗 {pii_type}'] = value
        elif 'BTC' in pii_type:
            pii_data['₿ BITCOIN'] = value[:20] + '...' if len(value) > 20 else value
        elif 'DOMAIN' in pii_type:
            pii_data['🌐 DOMAIN'] = value
        elif 'USERNAME' in pii_type:
            pii_data['👤 USERNAME'] = value
        elif 'COMPANY' in pii_type:
            self.company_intel['company'] = value.strip()
            pii_data['🏢 COMPANY'] = value.strip()
        elif 'API_KEY' in pii_type:
            pii_data['🔑 API KEY'] = value[:30] + '...'
        else:
            pii_data[pii_type] = value[:100]
    
    return pii_data if pii_data else {'TARGET': self.target}

def print_result(self, category, data, source, engine, link="", network="🌐"):
    with print_lock:
        emojis = {"BREACH": "💥", "KALI": "⚡", "SOCIAL": "📱", "CRYPTO": "₿", "USERNAME": "👤", "COMPANY": "🏢", "PASSWORD": "🔑"}
        emoji = emojis.get(category, "🌐")
        print(f"{Fore.GREEN}✓ [{emoji}] {Fore.CYAN}{category:10} | {Fore.YELLOW}{source:14} | {Fore.MAGENTA}{engine}")
        
        if isinstance(data, dict):
            for pii_type, pii_value in data.items():
                color = Fore.RED if any(x in pii_type.upper() for x in ['PASS', 'HASH', 'KEY']) else Fore.WHITE
                print(f"   🆔 {Fore.CYAN}{pii_type:12}: {color}{pii_value}")
        else:
            print(f"   🆔 {Fore.RED}→ {data}")
        
        print(f"   🔗 {Fore.BLUE}{link[:80]}...")
        print(f"{Style.RESET_ALL}")
        
        self.results.append({
            'category': category, 'data': data, 'source': source,
            'engine': engine, 'link': link if link.startswith('http') else f"https://google.com/search?q={urllib.parse.quote(self.target)}+{urllib.parse.quote(source)}",
            'network': network
        })
        
        self.update_pdf()

# FIXED PDF - PERFECT SIZE + ALL PII TYPES
def update_pdf(self):
    if not self.results:
        return
    
    clean_target = re.sub(r'[^\w\-_.]', '_', self.target)[:40]
    self.target_pdf = f"{TARGET_FOLDER}/{clean_target}.pdf"
    
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{self.target} - FULL OSINT ({len(self.results)} Records)</title>
<style>
body{{font-family:'Consolas','Courier New',monospace;background:linear-gradient(135deg,#0a0e17 0%,#1a2332 100%);color:#e6edf3;font-size:9.5px;line-height:1.3;padding:25px;max-width:100%;margin:0;overflow-x:auto;}}
h1{{color:#00d4aa;font-size:22px;text-align:center;margin:0 0 35px 0;font-weight:900;text-shadow:0 0 20px rgba(0,212,170,0.7);letter-spacing:2px;}}
h2{{color:#ff6b6b;font-size:14px;border-bottom:3px solid #1a2332;padding-bottom:12px;margin:35px 0 25px 0;letter-spacing:1.5px;position:relative;}}
h2::after{{content:'';position:absolute;bottom:-6px;left:0;width:60px;height:4px;background:linear-gradient(90deg,#00d4aa,#ff6b6b);border-radius:2px;}}
.stats-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin:30px 0;background:rgba(26,35,50,0.95);padding:30px;border-radius:20px;box-shadow:0 15px 50px rgba(0,0,0,0.6);backdrop-filter:blur(20px);}}
.stat-card{{text-align:center;padding:25px;background:linear-gradient(145deg,#1a2332 0%,#2d4059 100%);border-radius:16px;border:2px solid rgba(0,212,170,0.3);box-shadow:0 10px 40px rgba(0,212,170,0.2);transition:all 0.4s ease;}}
.stat-card:hover{{transform:translateY(-5px);box-shadow:0 20px 60px rgba(0,212,170,0.4);border-color:#00d4aa;}}
.stat-number{{font-size:32px;font-weight:900;color:#00d4aa;margin-bottom:10px;text-shadow:0 0 15px rgba(0,212,170,0.8);}}
.stat-label{{font-size:12px;color:#a0b3c6;font-weight:600;letter-spacing:1px;text-transform:uppercase;}}
.results-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin:30px 0;}}
.pii-card{{background:linear-gradient(145deg,#1a2332 0%,#212b40 100%);padding:22px;border-radius:18px;border-left:6px solid #00d4aa;transition:all 0.4s cubic-bezier(0.25,0.46,0.45,0.94);box-shadow:0 8px 35px rgba(0,0,0,0.6);position:relative;overflow:hidden;max-height:220px;}}
.pii-card:hover{{transform:translateY(-8px) scale(1.02);box-shadow:0 20px 60px rgba(0,212,170,0.4);border-left-color:#ff6b6b;border-left-width:8px;}}
.pii-card.critical{{border-left-color:#ff4757 !important;}}
.pii-card.critical:hover{{box-shadow:0 20px 60px rgba(255,71,87,0.5) !important;}}
.pii-type{{font-weight:900;color:#00d4aa;font-size:11px;margin-bottom:12px;text-transform:uppercase;letter-spacing:1.5px;display:flex;align-items:center;font-family:monospace;}}
.pii-type.critical{{color:#ff4757 !important;}}
.pii-value{{font-family:monospace;background:rgba(10,14,23,0.9);padding:15px;border-radius:12px;font-size:10px;color:#f8f9fa;border:2px solid rgba(45,64,89,0.8);font-weight:700;word-break:break-word;line-height:1.5;max-height:80px;overflow-y:auto;box-shadow:inset 0 2px 10px rgba(0,0,0,0.5);}}
.pii-value.hash{{font-family:'Roboto Mono',monospace;font-size:9px;background:rgba(255,71,87,0.1);border-color:rgba(255,71,87,0.3);color:#ff9aa2;}}
.link-btn{{display:inline-block;background:linear-gradient(45deg,#00d4aa 0%,#0099cc 100%);color:#000;font-weight:800;font-size:10px;padding:10px 18px;margin-top:15px;border-radius:25px;text-decoration:none;transition:all 0.4s cubic-bezier(0.25,0.46,0.45,0.94);box-shadow:0 6px 25px rgba(0,212,170,0.5);text-transform:uppercase;letter-spacing:1px;position:relative;overflow:hidden;}}
.link-btn::before{{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent, rgba(255,255,255,0.4), transparent);transition:0.5s;}}
.link-btn:hover::before{{left:100%;}}
.link-btn:hover{{background:linear-gradient(45deg,#ff6b6b,#ff8e8e);transform:scale(1.08);box-shadow:0 12px 40px rgba(255,107,107,0.6);color:#fff !important;text-shadow:0 0 10px rgba(255,255,255,0.8);}}
.source-bar{{font-size:10px;color:#64748b;margin-top:15px;display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-top:2px solid rgba(26,35,50,0.8);font-family:monospace;letter-spacing:0.5px;}}
.company-section{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:40px;border-radius:25px;margin:40px 0;box-shadow:0 20px 70px rgba(102,126,234,0.5);border:2px solid rgba(255,255,255,0.2);position:relative;overflow:hidden;}}
.company-section::before{{content:'';position:absolute;top:0;left:0;right:0;height:6px;background:linear-gradient(90deg,#00d4aa,#ff6b6b,#667eea);}}
.footer{{text-align:center;font-size:10px;color:#64748b;margin-top:60px;padding-top:40px;border-top:4px solid #1a2332;padding-bottom:30px;font-family:monospace;letter-spacing:1px;}}
@media print{{body{{font-size:9px;background:white;color:black;}}h1{{color:#0066cc;}}h2{{color:#cc0000;border-bottom:2px solid #ccc;}}a{{color:#0066cc !important;background:none !important;box-shadow:none !important;}}.pii-grid{{grid-template-columns:repeat(6,1fr) !important;gap:8px !important;}}}}
@media screen and (max-width: 1200px) {{.results-grid{{grid-template-columns:repeat(auto-fill,minmax(350px,1fr));}}}}
@media screen and (max-width: 768px) {{.results-grid{{grid-template-columns:1fr;}}body{{font-size:11px;padding:15px;}}}}
</style>
</head>
<body>
<h1>🎯 {self.target} - COMPLETE OSINT ({len(self.results)} Records Found)</h1>

<div class="stats-grid">
<div class="stat-card"><div class="stat-number">{len(self.results)}</div><div class="stat-label">TOTAL HITS</div></div>
<div class="stat-card"><div class="stat-number">{len(set([r['source'] for r in self.results]))}</div><div class="stat-label">SOURCES</div></div>
<div class="stat-card"><div class="stat-number">{len([r for r in self.results if any(x in str(r.get('data','')).upper() for x in ['PASS','HASH','KEY'])])}</div><div class="stat-label">CREDS FOUND</div></div>
<div class="stat-card"><div class="stat-number">{datetime.now().strftime('%H:%M:%S')}</div><div class="stat-label">COMPLETE</div></div>
</div>'''

    if self.company_intel.get('company'):
        html += f'''<div class="company-section">
<h2 style="color:#fff;margin:0 0 25px 0;font-size:18px;">🏢 TARGET COMPANY INTEL</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:25px;">
<div class="pii-card" style="border-left-color:#667eea;">
<div class="pii-type">🏢 PRIMARY COMPANY</div>
<div class="pii-value">{self.company_intel['company']}</div>
</div>
</div></div>'''

    html += f'<h2>🆔 ALL PII + CREDS ({len(self.results)} Records)</h2><div class="results-grid">'

    for result in self.results[-50:]:  # Last 50 for size control
        pii_items = []
        if isinstance(result['data'], dict):
            for pii_type, pii_value in result['data'].items():
                is_critical = any(x in pii_type.upper() for x in ['PASS', 'HASH', 'KEY', 'API'])
                pii_items.append(f'''
<div class="pii-card {'critical' if is_critical else ''}">
<div class="pii-type {'critical' if is_critical else ''}">{"🔴" if is_critical else "🔵"} {pii_type}</div>
<div class="pii-value {'hash' if 'HASH' in pii_type else ''}">{pii_value}</div>
<a href="{result['link']}" target="_blank" class="link-btn" title="{result['link']}">🔗 VERIFY SOURCE</a>
<div class="source-bar">
<span>📡 {result["source"]}</span>
<span>⚙️ {result["engine"]}</span>
<span>{result["network"]}</span>
</div>
</div>''')
        html += "".join(pii_items)

    html += f'''</div>
<div class="footer">
<strong>KhalidHusain786 v85.7</strong> | {len(self.results)} Total Records | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC<br>
<i>🔗 ALL LINKS CLICKABLE • 📱 Mobile Optimized • 🖨️ Print Ready • UNLIMITED SIZE</i>
</div>
</body>
</html>'''
    
    try:
        from weasyprint import HTML
        HTML(string=html, base_url='file://' + os.getcwd() + '/').write_pdf(
            self.target_pdf,
            stylesheets=None,
            optimize_size='pdfa'  # FIXED: Perfect size optimization
        )
    except:
        html_file = self.target_pdf.replace('.pdf', '.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
