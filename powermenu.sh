#!/usr/bin/env bash

# Options with icons
options="󰌾 Lock\n󰍃 Logout\n󰑐 Reboot\n󰐥 Shutdown"

chosen=$(echo -e "$options" | rofi -dmenu -i -p "System" -theme ~/.config/qtile/powermenu.rasi)

case "$chosen" in
    *Lock*)
	i3lock -i ~/.config/qtile/wp/lockscreen.png
        ;;
    *Logout*)
        qtile cmd-obj -o cmd -f shutdown
        ;;
    *Reboot*)
        systemctl reboot
        ;;
    *Shutdown*)
        systemctl poweroff
        ;;
esac
