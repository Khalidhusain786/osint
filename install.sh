#!/bin/bash
# KHALID HUSAIN786 OSINT v90.0 BASH - SOCIAL + DOCS + LIVE CARDS ULTRA PRO
# ALL SOCIAL • USERNAMES • PASSWORDS • AADHAAR • DOC EXTRACT • LIVE BIN

set -euo pipefail

# COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# GLOBALS
TARGET=""
LIVECARDS=0
SOCIAL=0
DOCS=0
TARGET_FOLDER=""
TIMESTAMP=$(date +'%H:%M:%S')

banner() {
    clear
    cat << "EOF"

╔══════════════════════════════════════════════════════════════════════════════╗
║KHALID HUSAIN786 v90.0 BASH - SOCIAL+DOCS+LIVE CARDS ULTRA ENTERPRISE       ║
║ALL SOCIAL•USERNAMES•PASSWORDS•AADHAAR•DOC EXTRACT•LIVE BIN BANK            ║
╚══════════════════════════════════════════════════════════════════════════════╝

⚡ SOCIAL USERNAMES+PASSWORDS • AADHAAR/PHONE/DOCS • LIVE USABLE CARDS
📁 $TARGET_FOLDER | CARDS: $LIVECARDS | SOCIAL: $SOCIAL
EOF
}

luhn_check() {
    local card="$1"
    card=$(echo "$card" | tr -d ' -_')
    local len=${#card}
    if [ $len -lt 13 ] || [ $len -gt 19 ]; then
        echo "❌ DEAD"
        return 1
    fi
    
    local sum=0
    local i
    for ((i=$len-2; i>=0; i-=2)); do
        local d=$((10#${card:$i:1} * 2))
        sum=$((sum + (d/10) + (d%10)))
    done
    for ((i=$len-1; i>=0; i-=2)); do
        sum=$((sum + 10#${card:$i:1}))
    done
    [ $((sum % 10)) -eq 0 ] && echo "✅ LIVE" || echo "❌ DEAD"
}

get_bin_info() {
    local bin="$1"
    local cache_file="bin_cache_$bin"
    
    if [ -f "$cache_file" ]; then
        cat "$cache_file"
        return
    fi
    
    local info
    info=$(curl -s --max-time 4 -A "Mozilla/5.0" "https://lookup.binlist.net/$bin" | \
           jq -r '.bank.name // "UNKNOWN", 
                  .country.name // "UNKNOWN", 
                  .bank.city // "UNKNOWN", 
                  .type // "DEBIT/CREDIT", 
                  .brand // "UNKNOWN"' 2>/dev/null || echo "UNKNOWN\nUNKNOWN\nUNKNOWN\nDEBIT/CREDIT\nUNKNOWN")
    
    echo -e "$info" > "$cache_file"
    cat "$cache_file"
}

validate_card() {
    local card="$1"
    local source="$2"
    
    card=$(echo "$card" | tr -d ' -_')
    local bin="${card:0:6}"
    local last4="${card: -4}"
    local masked="**** **** **** $last4"
    
    # CARD TYPE
    if [[ $card =~ ^4 ]]; then
        TYPE="🪙 VISA"
    elif [[ $card =~ ^5[1-5]|^2[2-7] ]]; then
        TYPE="🪙 MASTERCARD"
    elif [[ $card =~ ^3[47] ]]; then
        TYPE="🪙 AMEX"
    elif [[ $card =~ ^6 ]]; then
        TYPE="🪙 DISCOVER/RUPAY"
    else
        TYPE="❓ UNKNOWN"
    fi
    
    local status=$(luhn_check "$card")
    if [ "$status" = "✅ LIVE" ]; then
        read bank country city cardtype brand <<< $(get_bin_info "$bin")
        echo -e "${RED}💳 LIVE CARD #$((${LIVECARDS}+1)) $status${NC}"
        echo -e "   $YELLOW${TYPE:12s} | $CYAN$source${NC}"
        echo -e "   $WHITE Full:      $card${NC}"
        echo -e "   $WHITE Masked:    $masked${NC}"
        echo -e "   $GREEN Bank:      $bank${NC}"
        echo -e "   $BLUE Country:   $country | $city${NC}"
        echo -e "   $MAGENTA Type:      $cardtype${NC}"
        echo -e "   $YELLOW Network:   $brand${NC}"
        echo -e "   $GREEN ✅ USABLE: Amazon/Netflix/Flipkart/Spotify/Zomato/Paytm${NC}"
        
        ((LIVECARDS++))
        echo "$card|$TYPE|$masked|$bank|$country|$city|$cardtype|$brand|$source" >> "$CARDS_FILE"
    fi
}

extract_pii() {
    local text="$1"
    local source="$2"
    
    # CARDS
    echo "$text" | grep -E '\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b' | \
    while read card; do
        validate_card "$card" "$source"
    done
    
    # SOCIAL
    local social_hits
    social_hits=$(echo "$text" | grep -oE \
        "(twitter\.com|@)[a-zA-Z0-9_]{3,20}|facebook\.com/[a-zA-Z0-9._]{3,30}|instagram\.com/[a-zA-Z0-9._]{3,30}|t\.me/[a-zA-Z0-9_]{3,20}|reddit\.com/user/[a-zA-Z0-9_]{3,20}")
    
    if [ -n "$social_hits" ]; then
        echo -e "${MAGENTA}🐦 SOCIAL #$((SOCIAL+1))${NC}"
        echo -e "   $WHITE $social_hits | $CYAN$source${NC}"
        ((SOCIAL++))
        echo "$social_hits|$source|$TIMESTAMP" >> "$SOCIAL_FILE"
    fi
    
    # AADHAAR/PAN/PHONE
    local aadhaar=$(echo "$text" | grep -oE '\b(?:\d{4}[ -]?){3}\d{4}\b|\b\d{12}\b' | head -1)
    local pan=$(echo "$text" | grep -oE '[A-Z]{5}[0-9]{4}[A-Z]{1}' | head -1)
    local phone=$(echo "$text" | grep -oE '[6-9]\d{9}' | head -1)
    
    if [ -n "$aadhaar" ]; then
        echo -e "${BLUE}🆔 Aadhaar #$((DOCS+1))${NC}"
        echo -e "   $WHITE $aadhaar | $CYAN$source${NC}"
        ((DOCS++))
        echo "AADHAAR: $aadhaar|$source" >> "$DOCS_FILE"
    fi
    
    if [ -n "$pan" ]; then
        echo -e "${BLUE}🆔 PAN #$((DOCS+1))${NC}"
        echo -e "   $WHITE $pan | $CYAN$source${NC}"
        ((DOCS++))
        echo "PAN: $pan|$source" >> "$DOCS_FILE"
    fi
    
    if [ -n "$phone" ]; then
        echo -e "${BLUE}📱 PHONE #$((DOCS+1))${NC}"
        echo -e "   $WHITE $phone | $CYAN$source${NC}"
        ((DOCS++))
        echo "PHONE: $phone|$source" >> "$DOCS_FILE"
    fi
}

fast_scan() {
    local url="$1"
    local source="$2"
    local category="$3"
    
    echo -e "${GREEN}⚡ Scanning $CYAN$source${NC}"
    
    local content
    content=$(curl -s --max-time 7 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
        --insecure "$url" | head -c 500000)
    
    if [ -n "$content" ]; then
        extract_pii "$content" "$source"
    fi
}

scan_all_social() {
    banner
    echo -e "${RED}🐦 SCANNING ALL SOCIAL PLATFORMS...${NC}"
    
    local sites=(
        "Twitter:https://twitter.com/search?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')"
        "Facebook:https://www.facebook.com/search/top?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')"
        "Instagram:https://www.instagram.com/explore/search/keyword/?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')"
        "Telegram:https://t.me/s/$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')"
        "Reddit:https://www.reddit.com/search/?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')"
        "TikTok:https://www.tiktok.com/search?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')"
    )
    
    for site in "${sites[@]}"; do
        IFS=':' read -r name url <<< "$site"
        fast_scan "$url" "$name" "🐦 SOCIAL" &
        sleep 0.5
    done
    wait
}

scan_documents() {
    echo -e "${RED}📄 AADHAAR/PAN/DOCS SCAN...${NC}"
    
    local sites=(
        "GovDocs:https://www.google.com/search?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')+aadhaar+filetype:pdf"
        "IndiaGov:https://www.google.com/search?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')+site:gov.in"
        "PDFLeaks:https://www.google.com/search?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')+filetype:pdf+pan"
    )
    
    for site in "${sites[@]}"; do
        IFS=':' read -r name url <<< "$site"
        fast_scan "$url" "$name" "📄 DOCS" &
        sleep 0.5
    done
    wait
}

scan_card_leaks() {
    echo -e "${RED}💳 CARD LEAKS SCAN...${NC}"
    
    local sites=(
        "LeakIX:https://leakix.net/search/?q=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')"
        "BreachDir:https://breachdirectory.org/search?query=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9]/%/g')"
    )
    
    for site in "${sites[@]}"; do
        IFS=':' read -r name url <<< "$site"
        fast_scan "$url" "$name" "💳 LEAKS" &
        sleep 0.5
    done
    wait
}

generate_report() {
    clean_target=$(echo "$TARGET" | sed 's/[^a-zA-Z0-9._-]/_/g' | cut -c1-25)
    TARGET_FOLDER="./Target/${clean_target}"
    mkdir -p "$TARGET_FOLDER"
    
    CARDS_FILE="$TARGET_FOLDER/${clean_target}_LIVE_CARDS.txt"
    SOCIAL_FILE="$TARGET_FOLDER/${clean_target}_SOCIAL.txt"
    DOCS_FILE="$TARGET_FOLDER/${clean_target}_DOCS.txt"
    
    if [ $LIVECARDS -gt 0 ]; then
        echo -e "${GREEN}💳 $LIVECARDS LIVE CARDS → $CARDS_FILE${NC}"
    fi
    
    if [ $SOCIAL -gt 0 ]; then
        echo -e "${MAGENTA}🐦 $SOCIAL SOCIAL → $SOCIAL_FILE${NC}"
    fi
    
    if [ $DOCS -gt 0 ]; then
        echo -e "${BLUE}📄 $DOCS DOCS → $DOCS_FILE${NC}"
    fi
    
    echo -e "${GREEN}✅ COMPLETE REPORT: $TARGET_FOLDER/${NC}"
}

main() {
    if [ $# -ne 1 ]; then
        echo -e "${RED}Usage: $0 <target>${NC}"
        exit 1
    fi
    
    TARGET="$1"
    banner
    
    echo "==============================================="
    
    scan_all_social
    scan_documents
    scan_card_leaks
    
    echo -e "\n${RED}🎉 PENTEST COMPLETE | CARDS:$LIVECARDS | SOCIAL:$SOCIAL | DOCS:$DOCS${NC}"
    generate_report
}

main "$@"
