#!/usr/bin/env bash

# Rofi options
OPTIONS="1. Quick Scan (High-Risk Configs & Browsers)\n2. Full Home Directory Scan\n3. Rootkit Hunter Scan (rkhunter)\n4. Check Network Connections (ss)\n5. System Update & Upgrade (apt)"

# Select via Rofi
CHOICE=$(echo -e "$OPTIONS" | rofi -dmenu -i -p "Malware Scan" -theme ~/.config/qtile/scanner-avm.rasi)

# Target terminal runner (Kitty configured with class 'scanner-float')
TERM_CMD="kitty --class scanner-float -e bash -c"

mkdir -p "$HOME/Quarantine"

case "$CHOICE" in
    "1. Quick Scan (High-Risk Configs & Browsers)")
        $TERM_CMD "echo '=== Starting Quick ClamAV Scan ==='; \
        clamscan -r -i --move=$HOME/Quarantine \
            $HOME/.config/autostart \
            $HOME/.local/bin \
            $HOME/.local/share \
            $HOME/.cache \
            $HOME/.mozilla \
            $HOME/.config/BraveSoftware \
            $HOME/.config/google-chrome; \
        echo '--- Done. Press Enter to exit ---'; read line"
        ;;
    "2. Full Home Directory Scan")
        $TERM_CMD "echo '=== Starting Home Directory Scan (Skipping Large Files) ==='; \
        clamscan -r -i --max-filesize=100M --max-scansize=100M --move=$HOME/Quarantine $HOME/; \
        echo '--- Done. Press Enter to exit ---'; read line"
        ;;
    "3. Rootkit Hunter Scan (rkhunter)")
        $TERM_CMD "echo '=== Running Rootkit Hunter ==='; \
        sudo rkhunter --check --rwo; \
        echo '--- Done. Press Enter to exit ---'; read line"
        ;;
    "4. Check Network Connections (ss)")
        $TERM_CMD "echo '=== Listening Sockets & Active Connections ==='; \
        sudo ss -tulpn; \
        echo '---------------------------------------------'; \
        echo '=== Active Remote Connections ==='; \
        sudo ss -tunp state established; \
        echo '--- Done. Press Enter to exit ---'; read line"
        ;;
    "5. System Update & Upgrade (apt)")
        $TERM_CMD "echo '=== Updating Package Lists & Upgrading System ==='; \
        sudo apt update && sudo apt upgrade -y; \
        echo '--- Done. Press Enter to exit ---'; read line"
        ;;
    *)
        exit 0
        ;;
esac
