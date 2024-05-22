from django import template

register = template.Library()

@register.filter
def value_from_model(model, field):
    return getattr(model, field)


@register.filter
def get_verbose_name(obj):
    return obj.verbose_name.title()
@register.filter
def add_class(field, css_class):
    attrs = {"class": field.css_classes(css_class)}
    if field.field.widget.attrs.get("readonly"):
        attrs["readonly"] = "readonly"
    return field.as_widget(attrs=attrs)