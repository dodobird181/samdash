#!/usr/bin/bash

set -e

git pull origin main
systemctl --user restart samdash
if systemctl --user is-active --quiet samdash; then
    echo "Service is running."
    exit 0
else
    echo "Service is not running."
    exit 1
fi
