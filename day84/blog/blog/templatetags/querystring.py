from django import template
register = template.Library()

@register.simple_tag
def querystring(request, **kwargs):
    params = request.GET.copy()
    for k, v in kwargs.items():
        if v is None:
            params.pop(k, None)
        else:
            params[k] = v
    return params.urlencode()
