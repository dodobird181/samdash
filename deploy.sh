!/usr/bin/bash

git pull origin main
systemctl restart samdash
if systemctl is-active --quiet samdash; then
    echo "Service is running."
    exit 0
else
    echo "Service is not running."
    exit 1
fi
