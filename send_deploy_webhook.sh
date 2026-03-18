#!/usr/bin/bash

BODY='{}'
TIMESTAMP=$(date +%s)
SECRET="$MN_SERVER_DEPLOY_SECRET"
SIGNATURE=$(echo -n "$TIMESTAMP$BODY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d " " -f2)
curl -X POST https://sammorris.ca/deploy/samdash \
     -H "Content-Type: application/json" \
     -H "X-Timestamp: $TIMESTAMP" \
     -H "X-Signature: $SIGNATURE" \
     -d "$BODY"
