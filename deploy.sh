#!/usr/bin/bash

git pull origin main
sudo systemctl restart samdash
if sudo systemctl is-active --quiet samdash; then
    echo "Service is running."
    exit 0
else
    echo "Service is not running."
    exit 1
fi
