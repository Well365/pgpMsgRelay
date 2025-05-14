from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns

app_name = 'message_agent'

urlpatterns = [
    # 语言选择
    path('set_language/', views.set_language, name='set_language'),
    
    # 现有 Web 端点
    path('relay/', views.create_message, name='create_message'),
    path('relay/m/<str:short_id>/', views.view_message, name='view_message'),
    path('relay/m/<str:short_id>/password/', views.password_access, name='password_access'),
    
    # API 端点 - 面向移动客户端
    path('relay/api/messages/create/', views.api_create_message, name='api_create_message'),
    path('relay/api/messages/<str:short_id>/', views.api_get_message, name='api_get_message'),
    path('relay/api/messages/<str:short_id>/verify-password/', views.api_verify_password, name='api_verify_password'),
]
