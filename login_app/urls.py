from django.urls import path
from .import views

urlpatterns = [
    path('create_user',views.create_user),
    path('hash_password',views.hash_password),
    path('login_auth',views.login_auth),
    path('unlock_user',views.unlock_user),
]