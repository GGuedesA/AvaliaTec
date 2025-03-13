from django.shortcuts import redirect
from django.urls import reverse


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [reverse("accounts:login"), reverse("accounts:register")]
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect("accounts:login")
        return self.get_response(request)
