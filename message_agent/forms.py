from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PGPMessage

class PGPMessageForm(forms.ModelForm):
    class Meta:
        model = PGPMessage
        fields = ['content', 'expiry_minutes', 'one_time_view', 'note', 'password']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': _('粘贴 OpenPGP 加密信息...')}),
            'note': forms.TextInput(attrs={'placeholder': _('可选备注信息')}),
            'password': forms.PasswordInput(attrs={'placeholder': _('可选访问密码')}, render_value=True),
        }
        labels = {
            'content': _('OpenPGP 信息'),
            'expiry_minutes': _('过期时间'),
            'one_time_view': _('一次性查看'),
            'note': _('备注'),
            'password': _('访问密码'),
        }

class PasswordAccessForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('请输入访问密码')}),
        label=_('访问密码')
    )
