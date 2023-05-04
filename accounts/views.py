from django.shortcuts import render, HttpResponse
from .forms import LoginForm, RegistrationForm

# Create your views here.

def login_view(request):
    if request.method == "POST":
        form = LoginForm()
    else:
        form = LoginForm()

    context = {
        "form": form
    }
    return render(request, "pages/login.html", context)


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm()
    else:
        form = RegistrationForm()

    context = {
        "form": form
    }
    return render(request, "pages/registration.html", context)

