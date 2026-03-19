#!/usr/bin/bash

set -euo pipefail

USER="dodob"

echo "Pulling new code..."
git pull origin main

echo "Restarting service..."
sudo -u $USER XDG_RUNTIME_DIR=/run/user/$(id -u $USER) systemctl --user restart samdash
sleep 2  # in case service starts then crashes quickly

echo "Verifying it restarted alright..."
sudo -u $USER XDG_RUNTIME_DIR=/run/user/$(id -u $USER) systemctl --user is-active samdash
