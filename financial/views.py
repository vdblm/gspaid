from django.shortcuts import render


def live_currency(request):
    return render(request, "misc/home.html")
