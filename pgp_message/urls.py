from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Django内置的语言切换视图
    path('i18n/', include('django.conf.urls.i18n')),
    # 允许无语言前缀访问主要页面（如 relay）
    path('relay/', include('message_agent.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('message_agent.urls')),
    prefix_default_language=True
)
