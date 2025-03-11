from django.core.exceptions import PermissionDenied


def user_is(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == role:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return _wrapped_view

    return decorator
