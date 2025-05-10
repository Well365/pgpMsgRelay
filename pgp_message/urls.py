from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# 非国际化路径
urlpatterns = [
    # Django 内置的语言切换视图
    path('i18n/', include('django.conf.urls.i18n')),
    
    # 我们自定义的语言切换视图也放在非国际化路径中
    path('', include('message_agent.urls')),
]

# 国际化路径 - 现在暂时去掉，简化问题排查
# urlpatterns += i18n_patterns(
#     path('admin/', admin.site.urls),
#     prefix_default_language=False
# )

# 添加管理站点URL
urlpatterns.append(path('admin/', admin.site.urls))
