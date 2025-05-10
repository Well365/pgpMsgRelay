from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    添加CSS类到表单字段
    用法: {{ form.field|add_class:"form-control" }}
    """
    return value.as_widget(attrs={'class': arg})
