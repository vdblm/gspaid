from django.shortcuts import render


def about_us(request):
    return render(request, "misc/home.html")


def rules(request):
    return render(request, "misc/rules.html")
