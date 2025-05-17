#!/bin/bash

# === 配置 ===
# 本地项目根目录 (确保末尾没有斜杠)
LOCAL_PROJECT_DIR="/Users/maxwell/Documents/idears/pgpMsgRelay"
# 远程服务器用户和地址
REMOTE_USER_HOST="root@8.219.85.168"
# 远程服务器上项目的根目录 (Django 项目将部署在此)
REMOTE_PROJECT_DIR="/srv/message_relay_api"
# SSH 私钥文件路径
SSH_KEY="/Users/$(whoami)/Documents/idears/homepage/aliyun/s4key.pem"
# Gunicorn systemd 服务名称
GUNICORN_SERVICE_NAME="message_relay_gunicorn"
# Gunicorn socket 文件路径 (相对于 REMOTE_PROJECT_DIR)
GUNICORN_SOCKET_FILENAME="message_relay.sock"

# === 辅助函数：在远程服务器上执行命令 ===
remote_exec() {
    ssh -i "$SSH_KEY" "$REMOTE_USER_HOST" "$@"
}

echo "🚀 开始部署 pgpMsgRelay 到 $REMOTE_USER_HOST..."

# 1. 在远程服务器上创建项目目录 (如果不存在)
echo "确保远程项目目录 $REMOTE_PROJECT_DIR 存在..."
remote_exec "mkdir -p $REMOTE_PROJECT_DIR"


# 2. 同步项目文件到远程服务器
echo "🔄 同步项目文件到远程服务器..."
rsync -avz --delete --progress \
    --exclude ".git/" \
    --exclude "venv/" \
    --exclude "*.pyc" \
    --exclude "__pycache__/" \
    --exclude ".DS_Store" \
    --exclude "db.sqlite3" \
    --exclude "staticfiles/" \
    --exclude "static/" \
    --exclude "*.log" \
    -e "ssh -i '$SSH_KEY'" \
    "$LOCAL_PROJECT_DIR/" "$REMOTE_USER_HOST:$REMOTE_PROJECT_DIR/"

echo "🚀 开始首次部署初始化..."

# 3. 初始化数据库
remote_exec "cd $REMOTE_PROJECT_DIR && source venv/bin/activate && python manage.py makemigrations locker"
remote_exec "cd $REMOTE_PROJECT_DIR && source venv/bin/activate && python manage.py migrate"
remote_exec "cd $REMOTE_PROJECT_DIR && source venv/bin/activate && python manage.py collectstatic --noinput"

echo "✅ 首次部署初始化完成。"
