from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        change_password_url = reverse('admin:password_change')
        logout_url = reverse('admin:logout')

        if (
            request.path.startswith('/admin') and
            user.is_authenticated and
            getattr(user, 'must_change_password', False) and
            request.path not in [change_password_url, logout_url]
        ):
            return redirect(change_password_url)

        if (
            request.path == change_password_url and
            request.method == 'POST' and
            user.is_authenticated and
            getattr(user, 'must_change_password', False)
        ):
            user.must_change_password = False
            user.save()
            print(f"✅ must_change_password скинуто для {user.email}")

        return self.get_response(request)
