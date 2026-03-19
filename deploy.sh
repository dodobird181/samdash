#!/usr/bin/bash

set -euo pipefail

git pull origin main
sudo -u dodob systemctl --user restart samdash
sleep 2  # in case service starts then crashes quickly
sudo -u dodob systemctl --user is-active samdash
