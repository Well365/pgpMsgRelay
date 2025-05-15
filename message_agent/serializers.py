from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import PGPMessage

class PGPMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGPMessage
        fields = ['content', 'expiry_minutes', 'one_time_view', 'note', 'password']
    
    def validate_content(self, value):
        if len(value) > 20000:
            raise serializers.ValidationError(_('内容超过了最大允许大小 (20KB)。请减少内容后重试。'))
        return value

class PGPMessageResponseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = PGPMessage
        fields = ['short_id', 'url', 'expiry_minutes', 'one_time_view', 'created_at']
    
    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(f'message/{obj.short_id}')

class PGPMessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGPMessage
        fields = ['content', 'note', 'one_time_view', 'created_at']
