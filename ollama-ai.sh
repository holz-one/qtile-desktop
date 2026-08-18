#!/usr/bin/env bash

# Fetch installed models from Ollama (excluding header row)
MODELS=$(ollama list | awk 'NR>1 {print $1}')

# Check if Ollama is running / has models
if [ -z "$MODELS" ]; then
    notify-send "Ollama Error" "No models found or Ollama service is not running."
    exit 1
fi

# Select model via Rofi
CHOICE=$(echo -e "$MODELS" | rofi -dmenu -i -p "Run Ollama Local  Model" -theme ~/.config/qtile/ollama-ai.rasi)

# Exit if no selection was made (e.g., ESC pressed)
if [ -z "$CHOICE" ]; then
    exit 0
fi

# Launch floating Kitty terminal running the selected Ollama model
kitty --class scanner-float -e bash -c "ollama run $CHOICE"
