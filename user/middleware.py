from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.conf import settings
from django.http import response
import time
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect




# try:
#     from django.utils.deprecation import MiddlewareMixin
# except ImportError:
#     MiddlewareMixin = object




class ExpireAfterPeriodInactivity:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


    def process_view(self, request, view_func, view_args, view_kwargs):
        
        # Timeout is done only for authenticated logged in users.
        if request.user.is_authenticated:
            
            current_datetime = datetime.timestamp(datetime.now())
            
            print(request.session)
            print(current_datetime)
                
                # Timeout if idle time period is exceeded.
            if request.session.has_key('last_activity') and (current_datetime - request.session['last_activity']) > settings.SESSION_IDLE_TIMEOUT:
                print("it works !!!!!!!!")
                logout(request)
                messages.add_message(request, messages.ERROR, 'Your session has timed out.')
                return redirect('login')
                
                # Set last activity time in current session.
            else:
                request.session['last_activity'] = current_datetime  





# import subprocess as sub
# import re

# try:
#     from django.utils.deprecation import MiddlewareMixin
# except ImportError:
#     MiddlewareMixin = object


# SESSION_TIMEOUT_KEY = "_session_init_timestamp_"


# class SessionTimeoutMiddleware(MiddlewareMixin):
 

#     def findWholeWord(self, w):

#         return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#         p = sub.Popen(('sudo', 'tcpdump', '-l', '-s 0', '-vvv', '-n', '((udp port 67) and (udp[8:1] = 0x1))'), stdout=sub.PIPE)
#         for row in iter(p.stdout.readline, b''):
#             if findWholeWord('requested-ip')(row):
#                 print(row.split(' ')[-1])
#                 print('mac_______address')
#             elif findWholeWord('client-id')(row):
#                 print(row.split(' ')[-1])





#     def process_request(self, request):
#         if not hasattr(request, "session") or request.session.is_empty():
#             return

#         init_time = request.session.setdefault(SESSION_TIMEOUT_KEY, time.time())

#         expire_seconds = getattr(
#             settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
#         )

#         session_is_expired = time.time() - init_time > expire_seconds

#         if session_is_expired:
#             request.session.flush()
#             print("it works !!!")
#             return redirect_to_login(next=request.path)

#         expire_since_last_activity = getattr(
#             settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY", False
#         )
#         grace_period = getattr(
#             settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD", 1
#         )

#         if expire_since_last_activity and time.time() - init_time > grace_period:
#             request.session[SESSION_TIMEOUT_KEY] = time.time()

            
            
            