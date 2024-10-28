from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                # Convert the timestamp to an offset-aware datetime
                last_activity_aware = timezone.make_aware(timezone.datetime.fromtimestamp(last_activity))
                idle_time = timezone.now() - last_activity_aware
                if idle_time.seconds > settings.SESSION_IDLE_TIMEOUT:
                    logout(request)
                    return redirect(settings.LOGOUT_URL)
            request.session['last_activity'] = timezone.now().timestamp()
        return self.get_response(request)
