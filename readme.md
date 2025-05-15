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

确保你的系统已安装 Python 3.6.8 和 pip。

### 创建虚拟环境并安装依赖:
```bash
python3.6 -m venv venv  # 固定使用 Python 3.6.8
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

## 部署后访问与测试

1. **访问主站点**  
   在浏览器中访问：  
   - https://si4key.com  
   - https://www.si4key.com  

2. **API 测试**  
   - 静态文件测试:  
     https://si4key.com/api/pgpMsgRelay/static/  
     > ⚠️ 如果出现 403 Forbidden，说明 staticfiles 目录权限不足或目录为空。  
     > - 请确保服务器上的 `/srv/message_relay_api/staticfiles/` 目录存在且有可读静态文件。  
     > - 可通过 `python manage.py collectstatic` 收集静态文件，并检查目录权限：  
     >   ```bash
     >   source venv/bin/activate
     >   python manage.py collectstatic --noinput
     >   chmod -R 755 /srv/message_relay_api/staticfiles/
     >   ```
     > - 目录为空时访问也会 403，需有实际静态文件。

   - API 路由测试（如有接口，可用 curl 或 Postman 测试）:  
     https://si4key.com/api/pgpMsgRelay/your_api_path/

3. **服务器本地测试**  
   在服务器上可用 curl 检查服务是否正常：  
   ```bash
   curl -I https://si4key.com
   curl -I https://si4key.com/api/pgpMsgRelay/
   ```

4. **常见问题排查**  
   - 若页面无法访问，检查 nginx 和 gunicorn 服务状态：  
     ```bash
     sudo systemctl status nginx
     sudo systemctl status message_relay_gunicorn
     ```
   - 查看日志排查错误：  
     ```bash
     sudo tail -n 50 /var/log/nginx/error.log
     sudo journalctl -u message_relay_gunicorn -n 50
     ```

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
