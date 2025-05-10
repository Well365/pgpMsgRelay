from django.urls import path
from . import views

app_name = 'message_agent'

urlpatterns = [
    path('', views.create_message, name='create_message'),
    path('m/<str:short_id>/', views.view_message, name='view_message'),
    path('m/<str:short_id>/password/', views.password_access, name='password_access'),
]
