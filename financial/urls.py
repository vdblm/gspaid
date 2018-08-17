from django.conf.urls import url, include

from financial import views

app_name = 'financial'

urlpatterns = [
    url(r'^live_currency/', views.live_currency),
    url(r'^currency_converter/', views.currency_converter),
    url(r'^online_wallet/', views.online_wallet, name='online_wallet'),
    url(r'^charged/', views.charged, name='charged'),
    url(r'^changed/', views.changed, name='changed'),
    url(r'^internal_payment/', views.internal_payment, name='internal_payment')
]
