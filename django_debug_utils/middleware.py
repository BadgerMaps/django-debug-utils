from django.views.debug import technical_500_response
import sys
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.conf import settings

DEBUG = getattr(settings, 'DEBUG', True)

class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        #Bail out if we're probably running locally, so we don't obfuscate errors
        if DEBUG:
            return None
        users = cache.get('technical_error_users')
        if not users:
            skip = cache.get('no_technical_error_users')
            if skip:
                return None
            try:
                g = Group.objects.get(name='Technical Errors')
                users = g.user_set.all()
                cache.set('technical_error_users', users, 60)
            except Group.DoesNotExist:
                cache.set('no_technical_error_users', True, 60*60)
                return None
        if request.user in users and request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
        return None

class SuperUserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        """Same as UserBasedExceptionMiddleware but works for all superusers but without
        need of creating groups, having cache etc.
        """
        if DEBUG:
            return None
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
        return None
