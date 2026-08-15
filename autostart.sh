#!/usr/bin/env bash

# Start PipeWire audio daemons if not running
pipewire &
pipewire-pulse &
wireplumber &
