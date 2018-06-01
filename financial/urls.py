from django.conf.urls import url, include

from financial import views

urlpatterns = [
    url(r'^live_currency/', views.live_currency),
]
