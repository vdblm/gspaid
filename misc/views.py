from django.shortcuts import render


def about_us(request):
    return render(request, "misc/home.html")
