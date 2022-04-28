# utils.py
from re import compile
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
login_not_required_urls = [compile(expr) for expr in getattr(settings, 'LOGIN_NOT_REQUIRED_URLS', [])]
allowed_tenant_areas = [compile(expr) for expr in getattr(settings, 'ALLOWED_TENANT_AREA', [])]
allowed_employee_areas = [compile(expr) for expr in getattr(settings, 'ALLOWED_EMPLOYEE_AREA', [])]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
         
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in login_not_required_urls):
                return redirect('{}?next={}'.format(settings.LOGIN_URL, request.path))

        else:
            if request.user.is_tenant:

                path = request.path_info.lstrip('/')
                if not any(m.match(path) for m in allowed_tenant_areas):
                    return redirect('/tenant_dashboard/')
            if request.user.is_employee:
                path = request.path_info.lstrip('/')
                if not any(m.match(path) for m in allowed_employee_areas):
                    return redirect('/maintenance/')