from django.urls import path
from . import views
app_name = 'locker'

urlpatterns = [
    path('', views.lock_page, name='lock_page'), 
    path('lock_device/', views.lock_page, name='lock_page'),
    path('lock_device/<str:device_id>/', views.lock_page, name='lock_page'),
    path('lock_success/<str:device_id>/', views.lock_success, name='lock_success'),
    path('api/check_lock/<str:device_id>/', views.check_lock, name='check_lock'),
    path('api/confirm_lock/<str:device_id>/', views.confirm_lock, name='confirm_lock'),
    path('api/register_device/<str:device_id>/', views.register_device, name='register_device'),
    path('api/record_purchase/', views.record_purchase, name='record_purchase'),
    path('api/check_purchase/', views.check_purchase_status, name='check_purchase_status'),
]
