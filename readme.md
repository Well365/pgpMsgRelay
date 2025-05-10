# OpenPGP 中转站 + 短链接系统

这是一个可以安全存储和分享 OpenPGP 加密信息的 Web 应用。

## 功能

- 上传和存储 OpenPGP 加密信息
- 生成唯一短链接
- 设置消息过期时间（10分钟/1小时/1天）
- 支持一次性查看选项
- 可选的密码保护
- 支持添加备注信息

## 快速开始

### 准备工作

确保你的系统已安装 Python 3.8+ 和 pip。

### 创建虚拟环境并安装依赖:
```bash
python -m venv venv
source venv/bin/activate  # 在Windows上是 venv\Scripts\activate
pip install -r requirements.txt
```

### 项目配置
1. 确保项目结构完整，包含以下文件：
   - pgp_message/settings.py
   - pgp_message/urls.py
   - pgp_message/wsgi.py
   - pgp_message/asgi.py
   - message_agent/ 应用目录

### 初始化数据库:
```bash
python manage.py makemigrations message_agent
python manage.py migrate
```

### 创建超级用户(可选):
```bash
python manage.py createsuperuser
```

### 启动开发服务器:
```bash
python manage.py runserver
```

成功启动后，访问 http://127.0.0.1:8000/ 即可使用系统。

## 项目结构

- pgp_message/ - 主项目配置目录
- message_agent/ - 主应用目录
  - models.py - 数据模型
  - views.py - 视图函数
  - urls.py - URL 路由
  - forms.py - 表单处理
- templates/ - HTML 模板
- static/ - 静态文件

## 故障排除

如果遇到 WSGI 相关错误，请确认已正确创建 wsgi.py 文件，并配置了正确的 DJANGO_SETTINGS_MODULE。

## 贡献

欢迎提交 Pull Request 或创建 Issue 来改进这个项目。
