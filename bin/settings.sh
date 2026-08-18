#!/bin/bash

if [ -x /usr/bin/lxqt-config ]; then
	lxqt-config
	exit 0
elif [ -x /usr/bin/xfce4-settings-manager ]; then
	xfce4-settings-manager
	exit 0

fi
notify-send "No Settings App"
