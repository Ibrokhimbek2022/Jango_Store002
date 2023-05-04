from django.urls import path
from . import views

# accounts/login/
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("registration/", views.registration_view, name="registration")
]










