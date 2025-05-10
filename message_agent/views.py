from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import PGPMessage
from .forms import PGPMessageForm, PasswordAccessForm

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
    
    return render(request, 'message_agent/create_message.html', {'form': form})

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
