from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    添加CSS类到表单字段
    用法: {{ form.field|add_class:"form-control" }}
    """
    css_classes = value.field.widget.attrs.get('class', '')
    if css_classes:
        css_classes = f"{css_classes} {arg}"
    else:
        css_classes = arg
    return value.as_widget(attrs={'class': css_classes})
