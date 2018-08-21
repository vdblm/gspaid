from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def change_profile(request):
    return render(request, "edit_user_info/profile.html")


def changed_profile(request):
    return render(request, "edit_user_info/changed_profile.html")


def profile(request):
    return render(request, "edit_user_info/profile.html")
