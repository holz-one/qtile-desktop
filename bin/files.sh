#!/bin/bash

if [ -x /usr/bin/pcmanfm-qt ]; then
	pcmanfm-qt
	exit 0
elif [ -x /usr/bin/thunar ]; then
	thunar
	exit 0
else
	rofi -show filebrowser -theme ~/.config/qtile/apps.rasi
	exit 0
fi
