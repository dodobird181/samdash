On a computer with `$MN_SERVER_DEPLOY_SECRET` set, run the folowing command:

```

git push && \
sudo chmod +x send_deploy_webhook.sh && \
./send_deploy_webhook.sh

```