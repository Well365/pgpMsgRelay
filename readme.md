创建虚拟环境并安装依赖:
python -m venv venv
source venv/bin/activate  # 在Windows上是 venv\Scripts\activate
pip install -r requirements.txt

初始化数据库:
python manage.py makemigrations message_agent
python manage.py migrate
创建超级用户(可选):
python manage.py createsuperuser

启动开发服务器:
python manage.py runserver
