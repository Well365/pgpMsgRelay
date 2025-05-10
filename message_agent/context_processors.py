from django.conf import settings

def languages(request):
    """
    将语言设置添加到模板上下文
    """
    return {
        'LANGUAGES': settings.LANGUAGES,
        'LANGUAGE_CODE': request.LANGUAGE_CODE,
    }
