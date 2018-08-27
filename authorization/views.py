from django.contrib import messages
from django.shortcuts import render


# Create your views here.
from authorization.forms import UserForm


def index(request):
    return render(request, 'index.html')


def change_profile(request):
    print(request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.add_message(request, messages.INFO, 'Profile saved successfully!')
    else:
        user_form = UserForm(instance=request.user)
    return render(request, "edit_user_info/profile.html", {"user_form": user_form})


def changed_profile(request):
    return render(request, "edit_user_info/changed_profile.html")
