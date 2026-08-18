#!/usr/bin/env bash

# Base directories
SDIR="$HOME/.config/qtile"
WP="$SDIR/wp"
THEME="$SDIR/rofi_apps.rasi"

# Define menu items with mapped images from ~/.config/qtile/wp
OPTIONS="Apps\0icon\x1f${WP}/apps.png\n"
OPTIONS+="AppImage\0icon\x1f${WP}/appimage.jpeg\n"
OPTIONS+="Power\0icon\x1f${WP}/power.png\n"
OPTIONS+="Docker\0icon\x1f${WP}/docker.jpeg\n"
OPTIONS+="Ollama AI\0icon\x1f${WP}/ollama-ai.jpeg\n"
OPTIONS+="Scanner\0icon\x1f${WP}/scanner-avm.jpeg\n"
OPTIONS+="Services\0icon\x1f${WP}/srvdev.png\n"

# Prompt user via Rofi
CHOICE=$(echo -e "$OPTIONS" | rofi -dmenu \
    -i \
    -p "🚀 Qtile Hub" \
    -show-icons \
    -theme "$THEME")

# Execute selected script
case "$CHOICE" in
    "Apps")
        exec rofi -show drun -theme "$SDIR/apps.rasi" &
        ;;
    "AppImage")
        exec "$SDIR/appimage.sh" &
        ;;
    "Power")
        exec "$SDIR/powermenu.sh" &
        ;;
    "Docker")
        exec "$SDIR/docker.sh" &
        ;;
    "Ollama AI")
        exec "$SDIR/ollama-ai.sh" &
        ;;
    "Scanner")
        exec "$SDIR/scanner-avm.sh" &
        ;;
    "Services")
        exec "$SDIR/devsrv.sh" &
        ;;
    *)
        exit 0
        ;;
esac
