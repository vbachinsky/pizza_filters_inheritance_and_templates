from django.utils.deprecation import MiddlewareMixin
import time
from django.shortcuts import redirect
from django.contrib.auth import logout

MAXIMUM_IDDLE_TIME = 300

class SuperMiddlewareClass(MiddlewareMixin):
    def process_request(self, request):
        request_count = request.session.get('requests_count')
        request_start_time = request.session.get('start_time')
        if not request_count:
            request.session['requests_count'] = 1
            request.session['bane_time'] = None
            request.session['start_time'] = time.time()
        else:
            request.session['requests_count'] += 1
            if request.session.get('requests_count') > 50 and request.path != '/alarm/' and not request.session['bane_time']:
                delta_time = time.time() - request.session['start_time']
                if delta_time > 120:
                    request.session['start_time'] = time.time()
                    request.session['requests_count'] = 1
                else:
                    request.session['bane_time'] = time.time()
                    return redirect('/alarm/')
            else:
                if request.session['bane_time']:
                    delta_bane_time = time.time() - request.session['bane_time']
                    if delta_bane_time > 240:
                        request.session['bane_time'] = None

    def process_response(self, request, response):
        return response


class LogoutMiddlewareClass(MiddlewareMixin):
    def process_request(self, request):
        request_start_time = request.session.get('start_time')
        if request.user.is_authenticated:
            delta_time = time.time() - request.session['start_time']
            if delta_time > MAXIMUM_IDDLE_TIME:
                request_start_time = time.time()
                logout(request)
                return redirect('/')

    def process_response(self, request, response):
        return response