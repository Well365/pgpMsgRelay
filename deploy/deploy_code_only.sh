#!/bin/bash

# === 配置 ===
# 本地项目根目录 (确保末尾没有斜杠)
LOCAL_PROJECT_DIR="/Users/maxwell/Documents/idears/si4services/pgpMsgRelay"
# 远程服务器用户和地址
REMOTE_USER_HOST="root@8.219.85.168"
# 远程服务器上项目的根目录 (Django 项目将部署在此)
REMOTE_PROJECT_DIR="/srv/message_relay_api"
# SSH 私钥文件路径
SSH_KEY="/Users/$(whoami)/Documents/idears/homepage/aliyun/s4key.pem"

# === 辅助函数：在远程服务器上执行命令 ===
remote_exec() {
    ssh -i "$SSH_KEY" "$REMOTE_USER_HOST" "$@"
}

echo "🚀 开始部署代码和模型到 $REMOTE_USER_HOST..."

# 1. 同步代码和模型文件到远程服务器
echo "🔄 同步代码和模型文件到远程服务器..."
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
    -e 'ssh -i '"$SSH_KEY" \
    "$LOCAL_PROJECT_DIR/" "$REMOTE_USER_HOST:$REMOTE_PROJECT_DIR/"

if [ $? -ne 0 ]; then
  echo "❌ 文件同步失败！"
  exit 1
fi
echo "✅ 文件同步成功。"

# 2. 在远程服务器上迁移数据库
echo "⚙️  执行数据库迁移..."
remote_exec "cd $REMOTE_PROJECT_DIR && source venv/bin/activate && python manage.py migrate"

if [ $? -ne 0 ]; then
  echo "❌ 数据库迁移失败！"
  exit 1
fi
echo "✅ 数据库迁移成功。"

# 3. 重启 Gunicorn 服务
echo "🔄 重启 Gunicorn 服务..."
remote_exec "systemctl restart message_relay_gunicorn"

if [ $? -ne 0 ]; then
  echo "❌ Gunicorn 服务重启失败！"
  exit 1
fi
echo "✅ Gunicorn 服务重启成功。"

echo "✅ 部署完成，仅同步了代码和模型更改。"