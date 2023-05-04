from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "avatar", "password1", "password2"]
