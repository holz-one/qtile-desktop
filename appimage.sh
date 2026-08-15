#!/usr/bin/env bash

# Define the path where you store your game AppImages
GAMES_DIR="$HOME/Applications"

# Create the directory if it doesn't exist yet
mkdir -p "$GAMES_DIR" 2>/dev/null

# Theme configuration file path
THEME_FILE="$HOME/.config/qtile/appimage.rasi"

# 1. Grab all .AppImage files, strip the path/extension for a clean layout list
# 2. Pipe that list directly into Rofi using dmenu mode with the right-sidebar theme
SELECTION=$(find "$GAMES_DIR" -maxdepth 2 -type f -name "*.AppImage" -exec basename {} .AppImage \; | \
rofi -dmenu \
     -i \
     -p "⚔️ game:" \
     -theme "$THEME_FILE")

# If you hit Escape or close the menu, exit cleanly
if [ -z "$SELECTION" ]; then
    exit 0
fi

# Reconstruct the absolute path and fire the AppImage safely in the background
exec "$GAMES_DIR/$SELECTION.AppImage" &