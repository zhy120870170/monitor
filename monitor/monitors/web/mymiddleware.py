# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path != '/login' and request.path != '/login_in':
            if request.session.get('username', None):
                pass
            else:
                return HttpResponseRedirect('/login')
        else:
            pass

