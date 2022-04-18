from functools import wraps
from django.http import JsonResponse
from .models import Student,marks
from login_app import views
import time


def allowed_states(data):
    def decorator(func):
        def wrapper(request):
            for k,v in request.data.items():
                if type(v)==int:
                    return func(request)
                else:
                    return JsonResponse("Please send number",safe=False)
        return wrapper
    return decorator


def check_user_exists(data):
    def decorator(func):
        def wrapper(request):
            try:
                marks.objects.get(Roll_No=request.data["Roll_No"])
            except:
                return JsonResponse("Roll_number does not exists",safe=False)
            return func(request)
        return wrapper
    return decorator


def token_decorator(data):
    def decorator(func):
        def wrapper(request):
            if not 'HTTP_TOKEN' in request.META:
                return JsonResponse("Token should not be null please send the token",safe=False)
            try:   
                data = views.decode_and_take_username(request)
            except:
                return JsonResponse("INVALID TOKEN",safe=False)
            if data==True:
                return func(request)
        return wrapper
    return decorator


# def execution_time(data):
#     def decorator(func):
#         def wrapper(request):
#             start_time = time.time()

