import hashlib
from urllib.parse import urlencode
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def gravatar_url(email, size=40):
    default = "http://www.gravatar.com/avatar/?d=identicon"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower().encode("utf-8")).hexdigest(), urlencode({'d': default, 's': str(size)}))
