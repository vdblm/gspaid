from django.shortcuts import render


def live_currency(request):
    return render(request, "misc/home.html")


def currency_converter(request):
    return render(request, "misc/home.html")

