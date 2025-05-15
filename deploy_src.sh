#!/bin/bash

# 项目根目录
LOCAL_PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
REMOTE_USER_HOST="root@8.219.85.168"
REMOTE_PROJECT_DIR="/srv/message_relay_api"
SSH_KEY="/Users/$(whoami)/Documents/idears/homepage/aliyun/s4key.pem"

echo "本地项目目录: $LOCAL_PROJECT_DIR"
echo "远程服务器: $REMOTE_USER_HOST"
echo "远程项目目录: $REMOTE_PROJECT_DIR"

remote_exec() {
    ssh -i "$SSH_KEY" "$REMOTE_USER_HOST" "$@"
}

echo "同步 message_agent 到服务器..."
rsync -avz --delete --progress \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    -e "ssh -i '$SSH_KEY'" \
    "$LOCAL_PROJECT_DIR/message_agent/" "$REMOTE_USER_HOST:$REMOTE_PROJECT_DIR/message_agent/"

echo "同步 pgp_message 到服务器..."
rsync -avz --delete --progress \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    -e "ssh -i '$SSH_KEY'" \
    "$LOCAL_PROJECT_DIR/pgp_message/" "$REMOTE_USER_HOST:$REMOTE_PROJECT_DIR/pgp_message/"
echo "同步完成。"

echo "同步 locale 多语言 到服务器..."
rsync -avz --delete --progress \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    -e "ssh -i '$SSH_KEY'" \
    "$LOCAL_PROJECT_DIR/locale/" "$REMOTE_USER_HOST:$REMOTE_PROJECT_DIR/locale/"
echo "同步完成。"

echo "同步 staticfiles 到服务器..."
rsync -avz --delete --progress \
    --exclude "__pycache__/" \
    --exclude "*.pyc" \
    -e "ssh -i '$SSH_KEY'" \
    "$LOCAL_PROJECT_DIR/staticfiles/" "$REMOTE_USER_HOST:$REMOTE_PROJECT_DIR/staticfiles/"
echo "同步完成。"