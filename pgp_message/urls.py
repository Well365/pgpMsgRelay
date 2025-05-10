from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# 非国际化路径
urlpatterns = [
    # Django内置的语言切换视图（这个可以保留在非国际化路径中）
    path('i18n/', include('django.conf.urls.i18n')),
]

# 国际化路径 - 所有主要页面都应该支持语言前缀
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('message_agent.urls')),
    prefix_default_language=True  # 总是显示语言前缀，便于JavaScript处理
)
