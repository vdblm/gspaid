from django.shortcuts import render


# Create your views here.
from authorization.forms import UserForm


def index(request):
    return render(request, 'index.html')


def change_profile(request):
    user_form = UserForm()
    return render(request, "edit_user_info/profile.html", {"user_form": user_form})


def changed_profile(request):
    return render(request, "edit_user_info/changed_profile.html")
