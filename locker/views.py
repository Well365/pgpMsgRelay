from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import LockCommand, PurchaseRecord  # Import PurchaseRecord
import json
from datetime import datetime  # Import datetime

def lock_page(request, device_id=None):
    if device_id is None:
        # device_id 未填写，直接渲染页面让用户输入
        return render(request, 'locker/lock_page.html', {
            'device_id': '',
            'last_checked': None
        })
    # 获取或创建锁定命令
    lock_command, created = LockCommand.objects.get_or_create(device_id=device_id)
    
    if request.method == 'POST':
        # 设置锁定命令
        lock_command.should_lock = True
        lock_command.save()
        return redirect('lock_success', device_id=device_id)
    
    return render(request, 'locker/lock_page.html', {
        'device_id': device_id,
        'last_checked': lock_command.last_checked
    })

def lock_success(request, device_id):
    return render(request, 'locker/lock_success.html', {'device_id': device_id})

@csrf_exempt
def check_lock(request, device_id):
    try:
        # 获取锁定命令
        lock_command = get_object_or_404(LockCommand, device_id=device_id)
        
        # 返回是否应该锁定
        return JsonResponse({
            'should_lock': lock_command.should_lock,
            'device_id': device_id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def confirm_lock(request, device_id):
    try:
        # 获取锁定命令
        lock_command = get_object_or_404(LockCommand, device_id=device_id)
        
        if request.method == 'POST':
            # 重置锁定状态并标记为已检查
            lock_command.should_lock = False
            lock_command.mark_checked()
            # 修改数据库并保存
            lock_command.update_at_time()
            lock_command.save()
            
            return JsonResponse({'success': True})
        elif request.method == 'GET':
            # 处理 GET 请求 - 显示确认页面或直接确认锁定
            lock_command.should_lock = False
            lock_command.mark_checked()
            lock_command.update_at_time()
            lock_command.save()
            
            # 根据请求头判断是浏览器还是 API 请求
            if 'HTTP_ACCEPT' in request.META and 'text/html' in request.META['HTTP_ACCEPT']:
                try:
                    # 浏览器请求，返回确认页面
                    return render(request, 'locker/confirm_success.html', {
                        'device_id': device_id,
                        'last_checked': lock_command.last_checked
                    })
                except Exception as template_error:
                    # 如果模板出错，返回简单的成功信息
                    return JsonResponse({
                        'success': True, 
                        'message': f'Lock confirmed for device: {device_id}',
                        'template_error': str(template_error)
                    })
            else:
                # API请求，返回JSON
                return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 客户端发送锁定命令-通过 POST 请求或 GET 请求(浏览器)
@csrf_exempt
def lock_device(request, device_id):
    try:
        # 获取锁定命令
        lock_command = get_object_or_404(LockCommand, device_id=device_id)
        
        if request.method == 'POST':
            # 修改数据库并保存
            lock_command.should_lock = True
            lock_command.update_at_time()
            lock_command.save()
            
            return JsonResponse({'success': True})
        elif request.method == 'GET':
            # 处理 GET 请求 - 显示确认页面或直接确认锁定
            lock_command.should_lock = True
            lock_command.update_at_time()
            lock_command.save()
            
            # 根据请求头判断是浏览器还是 API 请求
            if 'HTTP_ACCEPT' in request.META and 'text/html' in request.META['HTTP_ACCEPT']:
                try:
                    # 浏览器请求，返回确认页面
                    return render(request, 'locker/confirm_success.html', {
                        'device_id': device_id,
                        'last_checked': lock_command.last_checked
                    })
                except Exception as template_error:
                    # 如果模板出错，返回简单的成功信息
                    return JsonResponse({
                        'success': True, 
                        'message': f'Lock confirmed for device: {device_id}',
                        'template_error': str(template_error)
                    })
            else:
                # API请求，返回JSON
                return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def register_device(request, device_id):
    try:
        # 获取锁定命令
        lock_command, created = LockCommand.objects.get_or_create(device_id=device_id)
        
        if request.method == 'POST':
            # 从POST数据中获取设备名称（如果有）
            try:
                data = json.loads(request.body)
                device_name = data.get('deviceName', 'Unknown Device')
                # 如果需要，可以在模型中添加device_name字段来存储这个值
            except:
                device_name = 'Unknown Device'
                
            # 记录设备注册
            lock_command.last_checked = timezone.now()
            lock_command.save()
            
            return JsonResponse({'success': True, 'message': f'Device {device_id} registered successfully'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def record_purchase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            device_id = data.get('device_id')
            product_id = data.get('product_id')
            transaction_id = data.get('transactionId')
            purchase_date_timestamp = data.get('purchase_date')  # Expecting Unix timestamp (seconds)
            original_transaction_id = data.get('original_transaction_id')  # Optional

            if not all([device_id, product_id, transaction_id, purchase_date_timestamp]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Convert timestamp to datetime object
            try:
                purchase_date = datetime.fromtimestamp(purchase_date_timestamp, tz=timezone.utc)
            except TypeError:  # Handle if timestamp is not a number
                return JsonResponse({'error': 'Invalid purchase_date format, expected Unix timestamp'}, status=400)

            # Check if this transaction has already been recorded to prevent duplicates
            if PurchaseRecord.objects.filter(transaction_id=transaction_id).exists():
                return JsonResponse({'success': True, 'message': 'Purchase already recorded'}, status=200)

            PurchaseRecord.objects.create(
                device_id=device_id,
                product_id=product_id,
                transaction_id=transaction_id,
                original_transaction_id=original_transaction_id,
                purchase_date=purchase_date
            )
            
            return JsonResponse({'success': True, 'message': 'Purchase recorded successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

@csrf_exempt
def check_purchase_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
            
        device_id = data.get('device_id')
        product_id_to_check = data.get('product_id')

        if not device_id or not product_id_to_check:
            return JsonResponse({'error': 'Missing device_id or product_id parameter'}, status=400)

        try:
            active_purchases = PurchaseRecord.objects.filter(product_id=product_id_to_check)

            if active_purchases.exists():
                latest_purchase = active_purchases.latest('purchase_date')
                return JsonResponse({
                    'isActive': True,
                    'device_id': device_id,
                    'product_id': product_id_to_check,
                    'message': f'An active purchase for product {product_id_to_check} is associated with the Apple ID (potentially on another device).',
                    'lastKnownPurchaseDateForProduct': latest_purchase.purchase_date.isoformat()
                })
            else:
                return JsonResponse({
                    'isActive': False,
                    'device_id': device_id,
                    'product_id': product_id_to_check,
                    'message': f'No active purchase record found for product {product_id_to_check} associated with this Apple ID.'
                })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)