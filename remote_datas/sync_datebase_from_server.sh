#!/bin/bash
# filepath: /Users/maxwell/Documents/idears/si4services/pgpMsgRelay/remote_datas/sync_datebase_from_server.sh
# 该脚本将远程服务器 /srv/message_relay_api 下的数据库同步到本地项目目录的 remote_datas 中，
# 每次同步时会在 remote_datas 目录下创建一个以当前日期(格式 YYYY-MM-DD)命名的目录，然后使用 scp 复制数据库文件。

# === 配置 ===
# 本地项目根目录 (确保末尾没有斜杠)
LOCAL_PROJECT_DIR="/Users/maxwell/Documents/idears/si4services/pgpMsgRelay"
# 远程服务器用户和地址
REMOTE_USER_HOST="root@8.219.85.168"
# 远程服务器上项目的根目录
REMOTE_PROJECT_DIR="/srv/message_relay_api"
# 数据库文件在远程服务器上的路径
REMOTE_DATABASE_FILE="$REMOTE_PROJECT_DIR/db.sqlite3"
# SSH 私钥文件路径
SSH_KEY="/Users/$(whoami)/Documents/idears/homepage/aliyun/s4key.pem"

# 同步目标根目录（位于本地项目目录下的 remote_datas）
TARGET_ROOT="$LOCAL_PROJECT_DIR/remote_datas"
# 以当前日期命名目录
CURRENT_DATE=$(date +%F)
TARGET_DIR="$TARGET_ROOT/$CURRENT_DATE"

# 确保目标目录存在
mkdir -p "$TARGET_DIR"

# 使用 scp 从远程服务器复制数据库文件到目标目录
scp -i "$SSH_KEY" "$REMOTE_USER_HOST:$REMOTE_DATABASE_FILE" "$TARGET_DIR/"

if [ $? -eq 0 ]; then
    echo "数据库同步成功，已复制到 $TARGET_DIR"
else
    echo "错误：无法从远程服务器复制数据库文件。"
    exit 1
fi