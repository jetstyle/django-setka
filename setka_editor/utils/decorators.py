from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods


def staff_and_certain_method_required(methods: list):
    def decorator(func):
        @require_http_methods(methods)
        @permission_required('is_stuff')
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

