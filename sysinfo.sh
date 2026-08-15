#!/bin/bash
if [ -f /usr/bin/neowofetch ]
then
	neowofetch

else
	fastfetch
fi
sleep 40
exit
