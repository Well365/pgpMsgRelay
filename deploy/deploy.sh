#!/bin/bash

# === 配置 ===
# 本地项目根目录 (确保末尾没有斜杠)
LOCAL_PROJECT_DIR="/Users/maxwell/Documents/idears/pgpMsgRelay"
# 远程服务器用户和地址
REMOTE_USER_HOST="root@8.219.85.168"
# 远程服务器上项目的根目录 (Django 项目将部署在此)
REMOTE_PROJECT_DIR="/root/message_relay_api"
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

if [ $? -ne 0 ]; then
  echo "❌ 文件同步失败！"
  exit 1
fi
echo "✅ 文件同步成功。"

# 3. 在远程服务器上执行设置步骤
echo "⚙️  在远程服务器上执行设置..."

# 3.1 备份并同步 nginx 配置
echo "📝 备份并同步 nginx 配置..."
remote_exec "cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$(date +%F-%T) || true"
remote_exec "cp -r /etc/nginx/conf.d /etc/nginx/conf.d.bak.$(date +%F-%T) || true"
remote_exec "mkdir -p /etc/nginx/conf.d"

# 3.2 上传 nginx 配置文件
remote_exec "cp $REMOTE_PROJECT_DIR/deploy/nginx/nginx.conf /etc/nginx/nginx.conf"
remote_exec "cp -r $REMOTE_PROJECT_DIR/deploy/nginx/conf.d/* /etc/nginx/conf.d/ 2>/dev/null || true"

# 3.3 上传 gunicorn systemd 服务文件
remote_exec "cp $REMOTE_PROJECT_DIR/deploy/message_relay_gunicorn.service /etc/systemd/system/message_relay_gunicorn.service"

# 3.4 重新加载 systemd 并重启服务
remote_exec "systemctl daemon-reload"
remote_exec "systemctl restart message_relay_gunicorn"
remote_exec "systemctl restart nginx"

echo "✅ 部署完成。"

