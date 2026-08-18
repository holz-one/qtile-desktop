#!/usr/bin/env bash
set -euo pipefail

TEMP_FILE=$(mktemp)
trap 'rm -f "$TEMP_FILE"' EXIT

SERVICES=(
    "docker.service|Docker Container Engine"
    "docker.socket|Docker Socket"
    "postgresql.service|PostgreSQL Database"
    #"mariadb.service|MariaDB/MySQL"
    "redis.service|Redis In-Memory Data Store"
    "mongod.service|MongoDB Database"
    "ollama.service|Ollama AI Server"
    "syncthing.service|Syncthing File Sync"
    "clamav-freshclam|Clam AV"
)

REAL_USER="${SUDO_USER:-$USER}"

echo "Removing old generated sudoers config files" 
sudo rm -f /etc/sudoers.d/{devsrv,qtile}-* 2>/dev/null 

for item in "${SERVICES[@]}"; do
    [[ "$item" =~ ^[[:space:]]*# ]] && continue

    IFS='|' read -r service name <<< "$item"

    # Skip service if it is not installed on this system (e.g., DietPi)
    if ! systemctl list-unit-files "$service" &>/dev/null; then
        echo "Skipping $service (Not installed on this host)"
        continue
    fi

    SAFE_NAME=$(echo "$service" | tr '.' '-')
    TARGET_FILE="/etc/sudoers.d/devsrv-${SAFE_NAME}"
    RULE_CONTENT="${REAL_USER} ALL=(ALL) NOPASSWD: /usr/bin/systemctl start ${service}, /usr/bin/systemctl stop ${service}"

    echo "$RULE_CONTENT" > "$TEMP_FILE"

    if sudo visudo -cf "$TEMP_FILE" &>/dev/null; then
        sudo install -m 0440 -o root -g root "$TEMP_FILE" "$TARGET_FILE"
        echo "✅ Installed: $TARGET_FILE ($name)"
    else
        echo "❌ Error syntax check failed for $service" >&2
    fi
done

# ####################################
# System Commands used in Rofi scripts
# ####################################
#
SYSCMD=(
	"ss"
	"apt update"
	"apt upgrade"
	"rkhunter"
	"freshclam"
)

for cmd in ${SYSCMD[@]}
do
    SAFE_NAME=$(echo "$cmd" | tr ' ' '-')
    RULE_CONTENT="${REAL_USER} ALL=(ALL) NOPASSWD: ${SAFE_NAME}" 
    TARGET_FILE="/etc/sudoers.d/qtile-${cmd}"
    echo "$RULE_CONTENT" > "$TEMP_FILE"

    if sudo visudo -cf "$TEMP_FILE" &>/dev/null; then
        sudo install -m 0440 -o root -g root "$TEMP_FILE" "$TARGET_FILE"
        echo "✅ Installed: $TARGET_FILE ($name)"
    else
        echo "❌ Error syntax check failed for $service" >&2
    fi

done
