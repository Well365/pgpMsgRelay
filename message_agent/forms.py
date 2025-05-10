from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import PGPMessage

class PGPMessageForm(forms.ModelForm):
    content = forms.CharField(
        label=_('OpenPGP 信息'),
        widget=forms.Textarea(attrs={'placeholder': _('粘贴 OpenPGP 加密信息...')}),
        max_length=20000,  # 限制最大字符数为 20K
    )
    
    note = forms.CharField(
        label=_('备注'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('可选备注信息')}),
    )
    
    password = forms.CharField(
        label=_('访问密码'),
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('可选访问密码')}),
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content) > 20000:
            raise ValidationError(_('内容超过了最大允许大小 (20KB)。请减少内容后重试。'))
        return content
    
    class Meta:
        model = PGPMessage
        fields = ['content', 'expiry_minutes', 'one_time_view', 'note', 'password']

class PasswordAccessForm(forms.Form):
    password = forms.CharField(
        label=_('访问密码'),
        widget=forms.PasswordInput(attrs={'placeholder': _('请输入访问密码')}),
    )
