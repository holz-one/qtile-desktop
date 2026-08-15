#!/usr/bin/env bash

# Check if brightnessctl exists and can actually find a controllable display
if ! command -v brightnessctl &>/dev/null || ! brightnessctl g &>/dev/null; then
    # Fallback/Silent exit for desktop monitors or SBCs (Orange Pi via HDMI) without sysfs backlights
    exit 0
fi

NOTIF_TAG="-h string:x-dunst-stack-tag:brightness"

get_brightness_pct() {
    brightnessctl -m | cut -d',' -f4 | tr -d '%'
}

case "$1" in
    up)
        brightnessctl set 5%+
        BRI=$(get_brightness_pct)
        notify-send $NOTIF_TAG "Brightness" "$BRI%" -i display-brightness -h int:value:"$BRI"
        ;;
    down)
        brightnessctl set 5%-
        BRI=$(get_brightness_pct)
        notify-send $NOTIF_TAG "Brightness" "$BRI%" -i display-brightness -h int:value:"$BRI"
        ;;
esac
