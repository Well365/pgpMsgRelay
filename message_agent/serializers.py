from rest_framework import serializers
from .models import PGPMessage

class PGPMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGPMessage
        fields = ['content', 'expiry_minutes', 'one_time_view', 'note', 'password']

class PGPMessageResponseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = PGPMessage
        fields = ['short_id', 'created_at', 'url']
        read_only_fields = fields
    
    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/m/{obj.short_id}/')
        return f'/m/{obj.short_id}/'

class PGPMessageDetailSerializer(serializers.ModelSerializer):
    requires_password = serializers.SerializerMethodField()
    
    class Meta:
        model = PGPMessage
        fields = ['content', 'created_at', 'note', 'one_time_view', 'requires_password']
    
    def get_requires_password(self, obj):
        return bool(obj.password)
