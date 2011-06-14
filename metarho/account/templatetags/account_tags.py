from django import template
import urllib, hashlib

from metarho import settings


GRAVATAR_BASEURL = getattr(settings, "GRAVATAR_BASEURL", "http://www.gravatar.com/avatar/")
GRAVATAR_DEFAULT_IMAGE = getattr(settings, "GRAVATAR_DEFAULT_IMAGE", "")
GRAVATAR_SIZE = getattr(settings, "GRAVATAR_SIZE", 40)

register = template.Library()

def gravitar_url(email, size):

    attrs = {
        'd': GRAVATAR_DEFAULT_IMAGE,
        's': size
    }

    gravatar_url = "%s%s/?" % (GRAVATAR_BASEURL, hashlib.md5(email.lower()).hexdigest())
    gravatar_url += urllib.urlencode(attrs)

    return {'gravatar': {'url': gravatar_url, 'size': size}}

@register.inclusion_tag('account/snippets/gravitar.xhtml')
def gravatar_for_email(email, size=GRAVATAR_SIZE):
    """
    Renders a gravatar image for user with the specified email via a template.

    {% gravatar_for_email "user@email.com" 40 %}

    :param email:  String representing the users email.
    :param size: Size of gravatar to use in pixels.  OPTIONAL
    
    """
    email = "%s" % email
    size = int(size)
    return gravitar_url(email, size)