from django.conf.urls import url, include

from workflow import views

urlpatterns = [
    url(r'^dashboard/', views.costumer_dashboard, name='dashboard'),
    url(r'^requests/', views.requests, name='requests'),
]
