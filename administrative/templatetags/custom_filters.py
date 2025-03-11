from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter
def split(value, key):
    """Divide a string pelo separador especificado."""
    return value.split(key)
