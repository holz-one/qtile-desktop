#!/usr/bin/env bash


nm-applet &
blueman-applet &

# Start PipeWire audio daemons if not running
systemctl --user restart pipewire pipewire-pilse wireplumber 

# pipewire &
# pipewire-pulse &
# wireplumber &

feh --bg-fill ~/.config/qtile/wp/bg.jpeg &
