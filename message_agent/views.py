from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import translation
from django.conf import settings
from .models import PGPMessage
from .forms import PGPMessageForm, PasswordAccessForm
from .serializers import (
    PGPMessageCreateSerializer, 
    PGPMessageResponseSerializer,
    PGPMessageDetailSerializer
)
import json

def create_message(request):
    if request.method == 'POST':
        form = PGPMessageForm(request.POST)
        if form.is_valid():
            pgp_message = form.save()
            full_url = request.build_absolute_uri(
                reverse('message_agent:view_message', args=[pgp_message.short_id])
            )
            return render(request, 'message_agent/message_created.html', {
                'short_url': full_url,
                'short_id': pgp_message.short_id
            })
    else:
        form = PGPMessageForm()
    
    context = {
        'form': form,
        'LANGUAGES': settings.LANGUAGES,  # 确保模板有语言列表
        'LANGUAGE_CODE': request.LANGUAGE_CODE,
    }
    return render(request, 'message_agent/create_message.html', context)

def view_message(request, short_id):
    try:
        message = get_object_or_404(PGPMessage, short_id=short_id)
        
        # 检查是否已过期
        if message.is_expired:
            message.delete()
            return render(request, 'message_agent/message_expired.html')
        
        # 检查是否需要密码访问
        if message.password:
            if 'password_verified' not in request.session or request.session['password_verified'] != short_id:
                return HttpResponseRedirect(reverse('message_agent:password_access', args=[short_id]))
        
        # 检查是否已被查看（一次性信息）
        if message.one_time_view and message.has_been_viewed:
            return render(request, 'message_agent/message_already_viewed.html')
        
        # 标记为已查看
        if message.one_time_view:
            message.has_been_viewed = True
            message.save()
        
        # 一次性信息，查看后删除
        delete_after_view = False
        if message.one_time_view:
            delete_after_view = True
        
        content = message.content
        
        if delete_after_view:
            message.delete()
        
        context = {
            'message': content,
            'note': message.note,
            'one_time': message.one_time_view,
        }
        
        if 'password_verified' in request.session and request.session['password_verified'] == short_id:
            del request.session['password_verified']
        
        return render(request, 'message_agent/view_message.html', context)
        
    except (Http404, ObjectDoesNotExist):
        return render(request, 'message_agent/message_not_found.html')

def password_access(request, short_id):
    try:
        message = get_object_or_404(PGPMessage, short_id=short_id)
        
        if request.method == 'POST':
            form = PasswordAccessForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['password'] == message.password:
                    request.session['password_verified'] = short_id
                    return HttpResponseRedirect(reverse('message_agent:view_message', args=[short_id]))
                else:
                    messages.error(request, '密码不正确')
        else:
            form = PasswordAccessForm()
        
        return render(request, 'message_agent/password_access.html', {'form': form, 'short_id': short_id})
        
    except (Http404, ObjectDoesNotExist):
        return render(request, 'message_agent/message_not_found.html')

# API 视图函数
@api_view(['POST'])
def api_create_message(request):
    """
    创建新的 PGP 加密消息 - API 端点
    """
    serializer = PGPMessageCreateSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.save()
        response_serializer = PGPMessageResponseSerializer(
            message, 
            context={'request': request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_get_message(request, short_id):
    """
    获取 PGP 加密消息 - API 端点
    """
    try:
        message = PGPMessage.objects.get(short_id=short_id)
        
        # 检查是否已过期
        if message.is_expired:
            message.delete()
            return Response(
                {"detail": "消息已过期并被删除。"},
                status=status.HTTP_410_GONE
            )
        
        # 检查是否需要密码
        if message.password:
            if 'password_verified' not in request.session or request.session['password_verified'] != short_id:
                return Response(
                    {"detail": "需要密码验证", "requires_password": True},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # 检查是否已被查看（一次性信息）
        if message.one_time_view and message.has_been_viewed:
            return Response(
                {"detail": "该消息已被查看过，不能重复查看。"},
                status=status.HTTP_410_GONE
            )
        
        # 标记为已查看
        if message.one_time_view:
            message.has_been_viewed = True
            message.save()
        
        serializer = PGPMessageDetailSerializer(message)
        
        # 一次性信息，查看后删除
        if message.one_time_view:
            message.delete()
        
        if 'password_verified' in request.session and request.session['password_verified'] == short_id:
            del request.session['password_verified']
            
        return Response(serializer.data)
        
    except PGPMessage.DoesNotExist:
        return Response(
            {"detail": "消息不存在或已被删除。"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
def api_verify_password(request, short_id):
    """
    验证加密消息密码 - API 端点
    """
    try:
        message = PGPMessage.objects.get(short_id=short_id)
        
        # 检查是否已过期
        if message.is_expired:
            message.delete()
            return Response(
                {"detail": "消息已过期并被删除。"},
                status=status.HTTP_410_GONE
            )
            
        data = request.data
        password = data.get('password')
        
        if not password:
            return Response(
                {"detail": "请提供密码。"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if password == message.password:
            request.session['password_verified'] = short_id
            return Response({"detail": "密码验证成功。"})
        else:
            return Response(
                {"detail": "密码不正确。"},
                status=status.HTTP_403_FORBIDDEN
            )
            
    except PGPMessage.DoesNotExist:
        return Response(
            {"detail": "消息不存在或已被删除。"},
            status=status.HTTP_404_NOT_FOUND
        )

def set_language(request):
    """
    设置用户界面语言
    """
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        print(f"Attempting to change language to: {lang_code}")  # 调试信息
        
        if lang_code and lang_code in [code for code, name in settings.LANGUAGES]:
            print(f"Language code {lang_code} is valid")
            
            # 设置会话语言
            translation.activate(lang_code)
            # 使用正确的会话键名称
            request.session[settings.LANGUAGE_SESSION_KEY] = lang_code
            print(f"Session language key set: {settings.LANGUAGE_SESSION_KEY}={lang_code}")
            
            # 获取引用页
            next_url = request.META.get('HTTP_REFERER', '/')
            print(f"Redirecting to: {next_url}")
            
            # 设置 Cookie
            response = HttpResponseRedirect(next_url)
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, 
                lang_code,
                max_age=365*24*60*60 if settings.LANGUAGE_COOKIE_AGE is None else settings.LANGUAGE_COOKIE_AGE
            )
            return response
        else:
            print(f"Invalid language code: {lang_code}")
            print(f"Valid codes are: {[code for code, name in settings.LANGUAGES]}")
    
    # 如果是 GET 请求或语言代码无效，则重定向回来源页面
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
