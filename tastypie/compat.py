from __future__ import unicode_literals

import django
from django.conf import settings
from django.utils.six.moves.urllib.parse import urlparse


__all__ = ['get_user_model', 'get_username_field', 'AUTH_USER_MODEL']

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Django 1.5+ compatibility
if django.VERSION >= (1, 5):
    def get_user_model():
        from django.contrib.auth import get_user_model as django_get_user_model

        return django_get_user_model()

    def get_username_field():
        return get_user_model().USERNAME_FIELD
else:
    def get_user_model():
        from django.contrib.auth.models import User

        return User

    def get_username_field():
        return 'username'


def get_module_name(meta):
    return getattr(meta, 'model_name', None) or getattr(meta, 'module_name')

# commit_on_success replaced by atomic in Django >=1.8
atomic_decorator = getattr(django.db.transaction, 'atomic', None) or getattr(django.db.transaction, 'commit_on_success')


PROTOCOL_TO_PORT = {
    'http': 80,
    'https': 443,
}


def same_origin(url1, url2):
    """
    Checks if two URLs are 'same-origin'
    """
    p1, p2 = urlparse(url1), urlparse(url2)
    try:
        o1 = (p1.scheme, p1.hostname, p1.port or PROTOCOL_TO_PORT[p1.scheme])
        o2 = (p2.scheme, p2.hostname, p2.port or PROTOCOL_TO_PORT[p2.scheme])
        return o1 == o2
    except (ValueError, KeyError):
        return False
