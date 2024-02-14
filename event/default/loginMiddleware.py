import re
from django.conf import settings
from django.shortcuts import redirect
from .helper import decide_type
from organizer.models import WebsiteSettings

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

if hasattr(settings, 'MAIN_EXEMPT_URLS'):
    M_EXEMPT_URLS = [re.compile(url) for url in settings.MAIN_EXEMPT_URLS]

"""
The exempt URLS for each type. This will allow them to 
bypass in certain specific scenarios.
"""
all_exempt_urls = {  # URLS that anyone should be able to access outside of their views
    r'profile',
}

hacker_exempt_URLS = {  # Any urls outside of hacker.views that they can access
    r'verifyphone',
}

organizer_exempt_URLS = {  # Any urls outside of organizer.views that they can access

}

not_organizer_exempt_URLS = {  # Any urls inside of organizer.views that regular Organizers can not access
    r'organizers',
}


"""
The modules for each type. Grants acces for a type to  
view every page in their module.
"""

hacker_mods = {
    "hacker.views",
}
organizer_mods = {
    "organizer.views",
}
head_organizer_not_mods = {
    "hacker.views",
}


HACKER_EXEMPT_URLS = [re.compile(url) for url in hacker_exempt_URLS]
ORGANIZER_EXEMPT_URLS = [re.compile(url) for url in organizer_exempt_URLS]
NOT_ORGANIZER_EXEMPT_URLS = [re.compile(url)for url in not_organizer_exempt_URLS]
ALL_EXEMPT_URLS = [re.compile(url) for url in all_exempt_urls]


class loginMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        site_mode = WebsiteSettings.objects.filter(
            waiting_list_status=True).exists()
        site_mode_exmpt_URLs = WL_EXEMPT_URLS if site_mode else EXEMPT_URLS
        url_is_exempt = any(url.match(path) for url in site_mode_exmpt_URLs)
        url_is_still_exempt = any(url.match(path) for url in EXEMPT_URLS)
        urls = ['login', 'register', 'reset-password']

        if any(url.match(path) for url in M_EXEMPT_URLS):
            return None
        user_type = decide_type(request.user)
        
        if request.user.is_authenticated and path in urls and user_type == 'hacker':
            return redirect('hacker-dash')
        elif request.user.is_authenticated and path in urls and user_type == 'head-organizer':
            return redirect('organizer-dash')
        elif request.user.is_authenticated or url_is_exempt:
            return None
        elif site_mode:
            return redirect('waitlist')
        else:
            return redirect('landing')


class accountsMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        module_name = view_func.__module__
        user = request.user
        path = request.path_info.lstrip('/')

        if path == 'logout/' or not request.user.is_authenticated:
            return None

        if any(url.match(path) for url in ALL_EXEMPT_URLS):
            return None
