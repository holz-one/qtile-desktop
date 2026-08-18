#!/usr/bin/env bash
# based on the guide from Rami Krispin
# https://github.com/RamiKrispin/awesome-ds-setting/blob/main/README.md
#
set -euo pipefail

echo "⚙️ Configuring Global Git Settings..."

# 1. Prompt for User Name
DEFAULT_NAME="$USER"
read -rp "Enter your Git Name [$DEFAULT_NAME]: " GIT_NAME
GIT_NAME="${GIT_NAME:-$DEFAULT_NAME}"

# 2. Prompt for User Email
DEFAULT_EMAIL="$USER@$HOST"
read -rp "Enter your Git Email [$DEFAULT_EMAIL]: " GIT_EMAIL
GIT_EMAIL="${GIT_EMAIL:-$DEFAULT_EMAIL}"

# 3. Apply Identity to Git Config
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

echo "👤 Configured Git Identity: $GIT_NAME <$GIT_EMAIL>"

# 4. Essential Modern Git Defaults for Linux
echo "🔧 Setting Linux Git performance and branch defaults..."

# Default initial branch name to main
git config --global init.defaultBranch main

# Auto-stash and rebase on pull to prevent merge commit clutter
git config --global pull.rebase true
git config --global rebase.autoStash true

# Colored terminal output
git config --global color.ui auto

# Remember credentials in memory for 2 hours (7200 seconds)
git config --global credential.helper 'cache --timeout=7200'

# Standardize line endings for Linux (LF)
git config --global core.autocrlf input

# 5. Optional SSH Key Generation
if [ ! -f "$HOME/.ssh/id_ed25519" ]; then
    echo "🔑 No SSH key found at ~/.ssh/id_ed25519."
    read -rp "Do you want to generate an ED25519 SSH key for GitHub? (y/N): " GEN_KEY
    if [[ "$GEN_KEY" =~ ^[Yy]$ ]]; then
        ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f "$HOME/.ssh/id_ed25519"
        echo "✅ SSH Key generated! Your public key:"
        cat "$HOME/.ssh/id_ed25519.pub"
    fi
else
    echo "🔑 Existing SSH key detected at ~/.ssh/id_ed25519"
fi

echo "✅ Git setup complete!"
