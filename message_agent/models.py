import random
import string
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator

def generate_short_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

class PGPMessage(models.Model):
    EXPIRY_CHOICES = [
        (10, _('10分钟')),
        (30, _('30分钟')),
        (60, _('1小时')),
        (240, _('4小时')),
    ]
    
    # TextField 添加最大长度限制为20K
    # 使用 validators 添加大小验证，而不是直接使用 max_length
    # 因为在某些数据库中，TextField 的 max_length 参数并不强制执行
    content = models.TextField(
        verbose_name=_('PGP加密信息'),
        validators=[MaxLengthValidator(20000)]
    )
    short_id = models.CharField(max_length=10, unique=True, default=generate_short_id, verbose_name=_('短链接ID'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('创建时间'))
    expiry_minutes = models.IntegerField(choices=EXPIRY_CHOICES, default=60, verbose_name=_('过期时间'))
    one_time_view = models.BooleanField(default=False, verbose_name=_('一次性查看'))
    has_been_viewed = models.BooleanField(default=False, verbose_name=_('已被查看'))
    note = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('备注'))
    password = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('访问密码'))
    
    @property
    def is_expired(self):
        if self.expiry_minutes is None:
            return False
        expiry_time = self.created_at + timezone.timedelta(minutes=self.expiry_minutes)
        return timezone.now() > expiry_time
    
    def __str__(self):
        return f"PGP Message {self.short_id}"
