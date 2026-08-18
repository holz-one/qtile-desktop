#!/usr/bin/env bash

# Tag for dunst/mako/swaync notification replacement (prevents spamming multiple bubbles)
NOTIF_TAG="-h string:x-dunst-stack-tag:volume"

# Function to get sink/source volume percentage and mute state
get_volume_info() {
    local target="$1"
    # Extract volume percentage (e.g., "0.55" -> "55") and check for [MUTED]
    local output
    output=$(wpctl get-volume "$target")
    
    local vol_raw
    vol_raw=$(echo "$output" | awk '{print $2}')
    
    # Calculate percentage using awk
    local vol_pct
    vol_pct=$(awk -v v="$vol_raw" 'BEGIN { printf "%.0f", v * 100 }')

    if echo "$output" | grep -q "MUTED"; then
        echo "MUTED $vol_pct"
    else
        echo "UNMUTED $vol_pct"
    fi
}

case "$1" in
    up)
        wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+ -l 1.0
        read -r state vol <<< "$(get_volume_info @DEFAULT_AUDIO_SINK@)"
        
        # Choose icon based on volume level
        if [ "$state" = "MUTED" ]; then
            notify-send $NOTIF_TAG "Volume Muted" "[$vol%]" -i audio-volume-muted -h int:value:"$vol"
        elif [ "$vol" -eq 0 ]; then
            notify-send $NOTIF_TAG "Volume" "0%" -i audio-volume-low -h int:value:0
        elif [ "$vol" -lt 50 ]; then
            notify-send $NOTIF_TAG "Volume" "$vol%" -i audio-volume-low -h int:value:"$vol"
        else
            notify-send $NOTIF_TAG "Volume" "$vol%" -i audio-volume-high -h int:value:"$vol"
        fi
        ;;

    down)
        wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
	read -r state vol <<< "$(get_volume_info @DEFAULT_AUDIO_SINK@)"
        
        if [ "$state" = "MUTED" ]; then
            notify-send $NOTIF_TAG "Volume Muted" "[$vol%]" -i audio-volume-muted -h int:value:"$vol"
        elif [ "$vol" -lt 50 ]; then
            notify-send $NOTIF_TAG "Volume" "$vol%" -i audio-volume-low -h int:value:"$vol"
        else
            notify-send $NOTIF_TAG "Volume" "$vol%" -i audio-volume-high -h int:value:"$vol"
        fi
        ;;

    mute)
        wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
        read -r state vol <<< "$(get_volume_info @DEFAULT_AUDIO_SINK@)"
        
        if [ "$state" = "MUTED" ]; then
            notify-send $NOTIF_TAG "Audio Muted" "Volume: $vol%" -i audio-volume-muted -h int:value:0
        else
            notify-send $NOTIF_TAG "Audio Unmuted" "Volume: $vol%" -i audio-volume-high -h int:value:"$vol"
        fi
        ;;

    mic-mute)
        wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle
        read -r state vol <<< "$(get_volume_info @DEFAULT_AUDIO_SOURCE@)"
        
        if [ "$state" = "MUTED" ]; then
            notify-send $NOTIF_TAG "Microphone Muted" "Input Disabled" -i microphone-sensitivity-muted
        else
            notify-send $NOTIF_TAG "Microphone Unmuted" "Input Active ($vol%)" -i audio-input-microphone
        fi
        ;;

    *)
        echo "Usage: $0 {up|down|mute|mic-mute}"
        exit 1
        ;;
esac
