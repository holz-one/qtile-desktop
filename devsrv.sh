#!/usr/bin/env bash

# Define the background services you care about
# Format: "systemd_service_name|User Friendly Display Name"
SERVICES=(
    "docker.service|Docker Container Engine"
    "postgresql.service|PostgreSQL Database"
    "mariadb.service|MariaDB/MySQL"
    "redis.service|Redis In-Memory Data Store"
    "mongodb.service|MongoDB Database"
    "ollama.service|Ollama AI Server"
    "syncthing.service|Syncthing File Sync"
)

# Services to STOP in Game Mode
GAME_MODE_TARGETS=(
    "docker.socket"
    "docker.service"
    "postgresql.service"
    "mariadb.service"
    "redis.service"
    "mongodb.service"
    "ollama.service"
    "syncthing.service"
)

# Function to check if a service is active
is_active() {
    systemctl is-active --quiet "$1"
}

# Function to build the Rofi menu string
build_menu() {
    echo "🎮 TOGGLE GAME MODE"
    echo "-----------------------------------"
    for item in "${SERVICES[@]}"; do
        IFS='|' read -r service name <<< "$item"
        if is_active "$service"; then
            echo "[RUNNING]  $name ($service)"
        else
            echo "[STOPPED]  $name ($service)"
        fi
    done
}

# Run Rofi and store selection
SELECTION=$(build_menu | rofi -dmenu -i -p "Services" -theme ~/.config/qtile/devsrv.rasi )

# Exit if no selection made
[ -z "$SELECTION" ] && exit 0

# Handle Game Mode activation
if [[ "$SELECTION" == *"TOGGLE GAME MODE"* ]]; then 
    sudo bash -c "
        for svc in ${GAME_MODE_TARGETS[*]}; do
            systemctl stop \$svc
        done
    "
    notify-send "🎮 Game Mode Enabled" "Background developer services have been stopped." -i controller
    exit 0
fi

#####
# Handle individual toggles
for item in "${SERVICES[@]}"; do
    IFS='|' read -r service name <<< "$item"
    if [[ "$SELECTION" == *"$service"* ]]; then
        if is_active "$service"; then
            if [[ "$service" == "docker.service" ]]; then
                sudo systemctl stop docker.socket docker.service
            else
                sudo systemctl stop "$service"
            fi
            notify-send "Service Manager" "Stopped $name" -i process-stop
        else
            if [[ "$service" == "docker.service" ]]; then
                sudo systemctl start docker.socket docker.service
            else
                sudo systemctl start "$service"
            fi
            notify-send "Service Manager" "Started $name" -i process-working
        fi
        break
    fi
done

