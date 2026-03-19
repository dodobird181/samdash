#!/usr/bin/bash

set -euo pipefail

USER="dodob"
git pull origin main
sudo -u $USER XDG_RUNTIME_DIR=/run/user/$(id -u $USER) systemctl --user restart samdash
sleep 2  # in case service starts then crashes quickly
sudo -u $USER XDG_RUNTIME_DIR=/run/user/$(id -u $USER) systemctl --user is-active samdash
