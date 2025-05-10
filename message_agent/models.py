import random
import string
from django.db import models
from django.utils import timezone

def generate_short_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

class PGPMessage(models.Model):
    EXPIRY_CHOICES = [
        (10, '10分钟'),
        (60, '1小时'),
        (1440, '1天'),
    ]
    
    content = models.TextField(verbose_name='PGP加密信息')
    short_id = models.CharField(max_length=10, unique=True, default=generate_short_id, verbose_name='短链接ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expiry_minutes = models.IntegerField(choices=EXPIRY_CHOICES, default=60, verbose_name='过期时间')
    one_time_view = models.BooleanField(default=False, verbose_name='一次性查看')
    has_been_viewed = models.BooleanField(default=False, verbose_name='已被查看')
    note = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')
    password = models.CharField(max_length=50, blank=True, null=True, verbose_name='访问密码')
    
    @property
    def is_expired(self):
        if self.expiry_minutes is None:
            return False
        expiry_time = self.created_at + timezone.timedelta(minutes=self.expiry_minutes)
        return timezone.now() > expiry_time
    
    def __str__(self):
        return f"PGP Message {self.short_id}"
