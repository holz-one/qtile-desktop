#!/usr/bin/env bash

# Rofi theme path (adjust if needed)
THEME="$HOME/.config/qtile/docker.rasi"

# Terminal wrapper (launches floating Kitty)
TERM_CMD="kitty --class scanner-float -e bash -c"

# Get format: "CONTAINER_ID | STATUS_ICON | CONTAINER_NAME (IMAGE)"
CONTAINER_LIST=$(docker ps -a --format '{{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Image}}' | awk -F'\t' '{
    status = ($3 ~ /^Up/) ? "🟢" : "🔴";
    printf "%s  %s  %s (%s)\n", $1, status, $2, $4
}')

if [ -z "$CONTAINER_LIST" ]; then
    notify-send "Docker Manager" "No Docker containers found."
    exit 0
fi

# Select container via Rofi
SELECTED_CONTAINER=$(echo -e "$CONTAINER_LIST" | rofi -dmenu -i -p "Docker Containers" -theme "$THEME")

[ -z "$SELECTED_CONTAINER" ] && exit 0

# Extract Container ID and Name
CONTAINER_ID=$(echo "$SELECTED_CONTAINER" | awk '{print $1}')
CONTAINER_NAME=$(echo "$SELECTED_CONTAINER" | awk '{print $3}')

# Container Actions Menu
ACTIONS="1. 🚀 Start Container\n2. 🛑 Stop Container\n3. 🔄 Restart Container\n4. 📜 View Logs (Follow)\n5. 💻 Shell Access (bash/sh)"

ACTION_CHOICE=$(echo -e "$ACTIONS" | rofi -dmenu -i -p "Action [$CONTAINER_NAME]" -theme "$THEME")

[ -z "$ACTION_CHOICE" ] && exit 0

case "$ACTION_CHOICE" in
    "1. 🚀 Start Container")
        docker start "$CONTAINER_ID" && notify-send "Docker" "Started $CONTAINER_NAME"
        ;;
    "2. 🛑 Stop Container")
        docker stop "$CONTAINER_ID" && notify-send "Docker" "Stopped $CONTAINER_NAME"
        ;;
    "3. 🔄 Restart Container")
        docker restart "$CONTAINER_ID" && notify-send "Docker" "Restarted $CONTAINER_NAME"
        ;;
    "4. 📜 View Logs (Follow)")
        $TERM_CMD "echo '=== Logs for $CONTAINER_NAME ==='; docker logs -f --tail 100 $CONTAINER_ID"
        ;;
    "5. 💻 Shell Access (bash/sh)")
        $TERM_CMD "docker exec -it $CONTAINER_ID bash || docker exec -it $CONTAINER_ID sh"
        ;;
    *)
        exit 0
        ;;
esac
