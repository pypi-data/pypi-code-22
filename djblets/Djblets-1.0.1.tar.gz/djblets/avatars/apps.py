"""The app configuration for djblets.avatars."""

from __future__ import unicode_literals

try:
    from django.apps import AppConfig
except ImportError:
    # Django < 1.7
    AppConfig = object


class AvatarsAppConfig(AppConfig):
    name = 'djblets.avatars'
    label = 'djblets_avatars'
