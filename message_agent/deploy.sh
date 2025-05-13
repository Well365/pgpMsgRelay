#!/bin/bash

# 项目根目录
LOCAL_PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE_USER_HOST="root@8.219.85.168"
REMOTE_PROJECT_DIR="/root/message_relay_api"
SSH_KEY="/Users/$(whoami)/Documents/idears/homepage/aliyun/s4key.pem"

remote_exec() {
    ssh -i "$SSH_KEY" "$REMOTE_USER_HOST" "$@"
}

echo "同步 message_agent 到服务器..."
rsync -avz --delete --progress \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    -e "ssh -i '$SSH_KEY'" \
    "$LOCAL_PROJECT_DIR/message_agent/" "$REMOTE_USER_HOST:$REMOTE_PROJECT_DIR/message_agent/"

echo "同步完成。"
