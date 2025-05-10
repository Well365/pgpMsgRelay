from django import forms
from .models import PGPMessage

class PGPMessageForm(forms.ModelForm):
    class Meta:
        model = PGPMessage
        fields = ['content', 'expiry_minutes', 'one_time_view', 'note', 'password']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': '粘贴 OpenPGP 加密信息...'}),
            'note': forms.TextInput(attrs={'placeholder': '可选备注信息'}),
            'password': forms.PasswordInput(attrs={'placeholder': '可选访问密码'}, render_value=True),
        }
        labels = {
            'content': 'OpenPGP 信息',
            'expiry_minutes': '过期时间',
            'one_time_view': '一次性查看',
            'note': '备注',
            'password': '访问密码',
        }

class PasswordAccessForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '请输入访问密码'}),
        label='访问密码'
    )
